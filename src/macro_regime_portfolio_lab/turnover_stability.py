from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Any

import pandas as pd

from macro_regime_portfolio_lab.backtest import MONTHS_PER_YEAR, calculate_metrics
from macro_regime_portfolio_lab.evaluation import run_regime_walk_forward
from macro_regime_portfolio_lab.validation import (
    add_validation_benchmarks,
    rolling_panel_sharpe_difference,
    summarize_validation_calendar_years,
    summarize_validation_metrics,
    summarize_validation_stress_periods,
    validation_bootstrap_checks,
)

POST_HOLDOUT_REVIEW_LABEL = "post-holdout-review diagnostic run"


@dataclass(frozen=True)
class TurnoverStabilityConfig:
    research_start: pd.Timestamp
    research_end: pd.Timestamp
    post_holdout_start: pd.Timestamp
    rolling_window_months: int
    cost_bps: float
    fallback_asset: str
    high_turnover_threshold: float
    turnover_metric_warmup_months: int
    hard_thresholds: dict[str, float]
    turnover_instability_penalty: float
    allocation_complexity_penalty: float
    switch_score_buffers: list[float]
    min_regime_history_values: list[int]
    top_n_values: list[int]
    max_monthly_turnover_values: list[float]
    report_label: str


@dataclass(frozen=True)
class TurnoverStabilityResult:
    selected_config: dict[str, float | int | str]
    candidate_grid: pd.DataFrame
    post_holdout_returns: pd.DataFrame
    post_holdout_metrics: pd.DataFrame
    post_holdout_calendar_years: pd.DataFrame
    post_holdout_stress_periods: pd.DataFrame
    post_holdout_bootstrap: pd.DataFrame
    report_label: str
    interpretation: str


def parse_turnover_stability_config(config: dict[str, Any]) -> TurnoverStabilityConfig:
    split = config["split"]
    selection = config["selection"]
    penalties = selection["objective_penalties"]
    return TurnoverStabilityConfig(
        research_start=pd.Timestamp(split["research_start"]),
        research_end=pd.Timestamp(split["research_end"]),
        post_holdout_start=pd.Timestamp(split["post_holdout_start"]),
        rolling_window_months=int(selection["rolling_window_months"]),
        cost_bps=float(selection["cost_bps"]),
        fallback_asset=str(selection["fallback_asset"]),
        high_turnover_threshold=float(selection["high_turnover_threshold"]),
        turnover_metric_warmup_months=int(selection["turnover_metric_warmup_months"]),
        hard_thresholds={
            key: float(value) for key, value in selection["hard_thresholds"].items()
        },
        turnover_instability_penalty=float(penalties["turnover_instability"]),
        allocation_complexity_penalty=float(penalties["allocation_complexity"]),
        switch_score_buffers=[float(value) for value in selection["switch_score_buffers"]],
        min_regime_history_values=[
            int(value) for value in selection["min_regime_history_values"]
        ],
        top_n_values=[int(value) for value in selection["top_n_values"]],
        max_monthly_turnover_values=[
            float(value) for value in selection["max_monthly_turnover_values"]
        ],
        report_label=str(config["report"]["label"]),
    )


def split_research_post_holdout(
    features: pd.DataFrame,
    next_returns: pd.DataFrame,
    config: TurnoverStabilityConfig,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    research_features = features.loc[config.research_start : config.research_end]
    research_returns = next_returns.loc[config.research_start : config.research_end]
    post_holdout_features = features.loc[config.post_holdout_start :]
    post_holdout_returns = next_returns.loc[config.post_holdout_start :]
    return research_features, research_returns, post_holdout_features, post_holdout_returns


def run_turnover_stability_protocol(
    features: pd.DataFrame,
    next_returns: pd.DataFrame,
    config: TurnoverStabilityConfig,
) -> TurnoverStabilityResult:
    research_features, research_returns, _, post_holdout_returns = (
        split_research_post_holdout(features, next_returns, config)
    )
    candidate_grid = build_turnover_stability_grid(
        research_features,
        research_returns,
        config,
    )
    selected_row = select_turnover_stable_candidate(candidate_grid)
    selected_config = {
        "switch_score_buffer": float(selected_row["switch_score_buffer"]),
        "min_regime_history": int(selected_row["min_regime_history"]),
        "top_n": int(selected_row["top_n"]),
        "max_monthly_turnover": float(selected_row["max_monthly_turnover"]),
        "turnover_metric_warmup_months": config.turnover_metric_warmup_months,
        "fallback_asset": config.fallback_asset,
        "cost_bps": config.cost_bps,
    }

    result = run_regime_walk_forward(
        features,
        next_returns,
        min_regime_history=int(selected_config["min_regime_history"]),
        top_n=int(selected_config["top_n"]),
        fallback_asset=str(selected_config["fallback_asset"]),
        cost_bps=float(selected_config["cost_bps"]),
        switch_score_buffer=float(selected_config["switch_score_buffer"]),
        max_monthly_turnover=float(selected_config["max_monthly_turnover"]),
    )
    full_returns = add_validation_benchmarks(
        result.returns,
        next_returns,
        cost_bps=config.cost_bps,
        fallback_asset=config.fallback_asset,
    )
    post_holdout_slice = full_returns.loc[
        post_holdout_returns.index.intersection(full_returns.index)
    ]
    post_holdout_metrics = summarize_validation_metrics(post_holdout_slice)
    interpretation = interpret_turnover_stability(
        selected_row=selected_row,
        post_holdout_metrics=post_holdout_metrics,
    )
    return TurnoverStabilityResult(
        selected_config=selected_config,
        candidate_grid=candidate_grid,
        post_holdout_returns=post_holdout_slice,
        post_holdout_metrics=post_holdout_metrics,
        post_holdout_calendar_years=summarize_validation_calendar_years(post_holdout_slice),
        post_holdout_stress_periods=summarize_validation_stress_periods(post_holdout_slice),
        post_holdout_bootstrap=validation_bootstrap_checks(post_holdout_slice),
        report_label=config.report_label,
        interpretation=interpretation,
    )


def build_turnover_stability_grid(
    research_features: pd.DataFrame,
    research_returns: pd.DataFrame,
    config: TurnoverStabilityConfig,
) -> pd.DataFrame:
    records = []
    for switch_score_buffer, min_regime_history, top_n, max_monthly_turnover in product(
        config.switch_score_buffers,
        config.min_regime_history_values,
        config.top_n_values,
        config.max_monthly_turnover_values,
    ):
        result = run_regime_walk_forward(
            research_features,
            research_returns,
            min_regime_history=min_regime_history,
            top_n=top_n,
            fallback_asset=config.fallback_asset,
            cost_bps=config.cost_bps,
            switch_score_buffer=switch_score_buffer,
            max_monthly_turnover=max_monthly_turnover,
        )
        returns = add_validation_benchmarks(
            result.returns,
            research_returns,
            cost_bps=config.cost_bps,
            fallback_asset=config.fallback_asset,
        )
        turnover_metrics = calculate_turnover_stability_metrics(
            returns["strategy_turnover"],
            high_turnover_threshold=config.high_turnover_threshold,
            warmup_months=config.turnover_metric_warmup_months,
        )
        rolling = rolling_panel_sharpe_difference(
            returns,
            window_months=config.rolling_window_months,
        )
        median_sharpe_difference = float(
            rolling["strategy_minus_best_benchmark_sharpe"].median()
        )
        turnover_instability = turnover_instability_score(turnover_metrics)
        allocation_complexity = allocation_complexity_score(top_n=top_n)
        selection_score = (
            median_sharpe_difference
            - config.turnover_instability_penalty * turnover_instability
            - config.allocation_complexity_penalty * allocation_complexity
        )
        metrics = calculate_metrics(
            returns["strategy_return_net"],
            periods_per_year=MONTHS_PER_YEAR,
        )
        record = {
            "switch_score_buffer": switch_score_buffer,
            "min_regime_history": min_regime_history,
            "top_n": top_n,
            "max_monthly_turnover": max_monthly_turnover,
            "turnover_metric_warmup_months": config.turnover_metric_warmup_months,
            "median_rolling_sharpe_difference": median_sharpe_difference,
            "turnover_instability_score": turnover_instability,
            "allocation_complexity_score": allocation_complexity,
            "selection_score": selection_score,
            "passes_turnover_stability": passes_turnover_thresholds(
                turnover_metrics,
                config.hard_thresholds,
            ),
            "research_start": returns.index.min(),
            "research_end": returns.index.max(),
            "research_months": len(returns),
            "strategy_sharpe": metrics["sharpe_ratio"],
            **turnover_metrics,
        }
        records.append(record)
    return pd.DataFrame.from_records(records).sort_values(
        by=["passes_turnover_stability", "selection_score", "average_turnover"],
        ascending=[False, False, True],
    )


def calculate_turnover_stability_metrics(
    turnover: pd.Series,
    *,
    high_turnover_threshold: float,
    warmup_months: int = 0,
) -> dict[str, float]:
    clean_turnover = turnover.dropna()
    if warmup_months < 0:
        raise ValueError("warmup_months must be non-negative.")
    if warmup_months:
        clean_turnover = clean_turnover.iloc[warmup_months:]
    if clean_turnover.empty:
        raise ValueError("Turnover stability metrics require at least one observation.")
    return {
        "average_turnover": float(clean_turnover.mean()),
        "turnover_p90": float(clean_turnover.quantile(0.90)),
        "turnover_p95": float(clean_turnover.quantile(0.95)),
        "high_turnover_month_share": float((clean_turnover > high_turnover_threshold).mean()),
        "turnover_volatility": float(clean_turnover.std(ddof=0)),
        "rolling_12m_average_turnover_max": float(
            clean_turnover.rolling(12, min_periods=1).mean().max()
        ),
    }


def turnover_instability_score(turnover_metrics: dict[str, float]) -> float:
    return float(
        turnover_metrics["turnover_p90"]
        + turnover_metrics["high_turnover_month_share"]
        + max(
            0.0,
            turnover_metrics["rolling_12m_average_turnover_max"]
            - turnover_metrics["average_turnover"],
        )
    )


def allocation_complexity_score(*, top_n: int) -> float:
    if top_n <= 3:
        return 0.0
    if top_n == 4:
        return 0.10
    return 0.20


def passes_turnover_thresholds(
    turnover_metrics: dict[str, float],
    hard_thresholds: dict[str, float],
) -> bool:
    return all(turnover_metrics[name] <= threshold for name, threshold in hard_thresholds.items())


def select_turnover_stable_candidate(candidate_grid: pd.DataFrame) -> pd.Series:
    eligible = candidate_grid[candidate_grid["passes_turnover_stability"]]
    if eligible.empty:
        raise ValueError("No candidate passed turnover-stability thresholds.")
    return eligible.sort_values(
        by=["selection_score", "average_turnover"],
        ascending=[False, True],
    ).iloc[0]


def interpret_turnover_stability(
    *,
    selected_row: pd.Series,
    post_holdout_metrics: pd.DataFrame,
) -> str:
    metrics = post_holdout_metrics.set_index("strategy")
    strategy = metrics.loc["regime_diagnostic_net"]
    equal_weight = metrics.loc["equal_weight_net"]
    shy = metrics.loc["shy_net"]
    if (
        selected_row["passes_turnover_stability"]
        and strategy["average_monthly_turnover"] <= selected_row["average_turnover"] * 1.5
    ):
        return "turnover_stability_reduced_known_failure_mode"
    if strategy["sharpe_ratio"] > equal_weight["sharpe_ratio"]:
        return "partial_post_holdout_review_diagnostic"
    if strategy["sharpe_ratio"] < shy["sharpe_ratio"]:
        return "failed_defensive_benchmark_hurdle"
    return "second_cycle_diagnostic_inconclusive"
