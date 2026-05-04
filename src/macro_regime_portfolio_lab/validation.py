from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Any

import pandas as pd

from macro_regime_portfolio_lab.backtest import MONTHS_PER_YEAR, calculate_metrics
from macro_regime_portfolio_lab.evaluation import run_regime_walk_forward
from macro_regime_portfolio_lab.robustness import (
    bootstrap_sharpe_difference,
    compound_return,
    max_drawdown,
    static_spy_tlt_6040_returns,
)


@dataclass(frozen=True)
class ValidationConfig:
    research_start: pd.Timestamp
    research_end: pd.Timestamp
    validation_start: pd.Timestamp
    rolling_window_months: int
    max_average_monthly_turnover: float
    cost_bps: float
    fallback_asset: str
    switch_score_buffers: list[float]
    min_regime_history_values: list[int]
    top_n_values: list[int]


@dataclass(frozen=True)
class ValidationResult:
    selected_config: dict[str, float | int | str]
    selection_grid: pd.DataFrame
    full_returns: pd.DataFrame
    validation_returns: pd.DataFrame
    validation_metrics: pd.DataFrame
    validation_calendar_years: pd.DataFrame
    validation_bootstrap: pd.DataFrame
    validation_stress_periods: pd.DataFrame
    interpretation: str


def parse_validation_config(config: dict[str, Any]) -> ValidationConfig:
    split = config["split"]
    selection = config["selection"]
    return ValidationConfig(
        research_start=pd.Timestamp(split["research_start"]),
        research_end=pd.Timestamp(split["research_end"]),
        validation_start=pd.Timestamp(split["validation_start"]),
        rolling_window_months=int(selection["rolling_window_months"]),
        max_average_monthly_turnover=float(selection["max_average_monthly_turnover"]),
        cost_bps=float(selection["cost_bps"]),
        fallback_asset=str(selection["fallback_asset"]),
        switch_score_buffers=[float(value) for value in selection["switch_score_buffers"]],
        min_regime_history_values=[
            int(value) for value in selection["min_regime_history_values"]
        ],
        top_n_values=[int(value) for value in selection["top_n_values"]],
    )


def split_research_validation(
    features: pd.DataFrame,
    next_returns: pd.DataFrame,
    config: ValidationConfig,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    research_features = features.loc[config.research_start : config.research_end]
    research_returns = next_returns.loc[config.research_start : config.research_end]
    validation_features = features.loc[config.validation_start :]
    validation_returns = next_returns.loc[config.validation_start :]
    return research_features, research_returns, validation_features, validation_returns


def run_validation_protocol(
    features: pd.DataFrame,
    next_returns: pd.DataFrame,
    config: ValidationConfig,
) -> ValidationResult:
    research_features, research_returns, _, validation_returns = split_research_validation(
        features,
        next_returns,
        config,
    )
    selection_grid = build_selection_grid(research_features, research_returns, config)
    selected_row = select_configuration(selection_grid)
    selected_config = {
        "switch_score_buffer": float(selected_row["switch_score_buffer"]),
        "min_regime_history": int(selected_row["min_regime_history"]),
        "top_n": int(selected_row["top_n"]),
        "fallback_asset": config.fallback_asset,
        "cost_bps": config.cost_bps,
    }

    result = run_regime_walk_forward(
        features,
        next_returns,
        min_regime_history=selected_config["min_regime_history"],
        top_n=selected_config["top_n"],
        fallback_asset=str(selected_config["fallback_asset"]),
        cost_bps=float(selected_config["cost_bps"]),
        switch_score_buffer=float(selected_config["switch_score_buffer"]),
    )
    full_returns = add_validation_benchmarks(
        result.returns,
        next_returns,
        cost_bps=config.cost_bps,
        fallback_asset=config.fallback_asset,
    )
    validation_slice = full_returns.loc[validation_returns.index.intersection(full_returns.index)]
    validation_metrics = summarize_validation_metrics(validation_slice)
    validation_calendar_years = summarize_validation_calendar_years(validation_slice)
    validation_bootstrap = validation_bootstrap_checks(validation_slice)
    validation_stress_periods = summarize_validation_stress_periods(validation_slice)
    interpretation = validation_interpretation(validation_metrics)
    return ValidationResult(
        selected_config=selected_config,
        selection_grid=selection_grid,
        full_returns=full_returns,
        validation_returns=validation_slice,
        validation_metrics=validation_metrics,
        validation_calendar_years=validation_calendar_years,
        validation_bootstrap=validation_bootstrap,
        validation_stress_periods=validation_stress_periods,
        interpretation=interpretation,
    )


def build_selection_grid(
    research_features: pd.DataFrame,
    research_returns: pd.DataFrame,
    config: ValidationConfig,
) -> pd.DataFrame:
    records = []
    for switch_score_buffer, min_regime_history, top_n in product(
        config.switch_score_buffers,
        config.min_regime_history_values,
        config.top_n_values,
    ):
        result = run_regime_walk_forward(
            research_features,
            research_returns,
            min_regime_history=min_regime_history,
            top_n=top_n,
            fallback_asset=config.fallback_asset,
            cost_bps=config.cost_bps,
            switch_score_buffer=switch_score_buffer,
        )
        returns = add_validation_benchmarks(
            result.returns,
            research_returns,
            cost_bps=config.cost_bps,
            fallback_asset=config.fallback_asset,
        )
        rolling = rolling_panel_sharpe_difference(
            returns,
            window_months=config.rolling_window_months,
        )
        objective = float(rolling["strategy_minus_best_benchmark_sharpe"].median())
        average_turnover = float(returns["strategy_turnover"].mean())
        metrics = calculate_metrics(
            returns["strategy_return_net"],
            periods_per_year=MONTHS_PER_YEAR,
        )
        equal_weight_metrics = calculate_metrics(
            returns["equal_weight_return_net"],
            periods_per_year=MONTHS_PER_YEAR,
        )
        static_6040_metrics = calculate_metrics(
            returns["static_60_40_return_net"],
            periods_per_year=MONTHS_PER_YEAR,
        )
        shy_metrics = calculate_metrics(
            returns["shy_return_net"],
            periods_per_year=MONTHS_PER_YEAR,
        )
        records.append(
            {
                "switch_score_buffer": switch_score_buffer,
                "min_regime_history": min_regime_history,
                "top_n": top_n,
                "selection_objective": objective,
                "average_strategy_turnover": average_turnover,
                "passes_turnover_constraint": average_turnover
                <= config.max_average_monthly_turnover,
                "research_start": returns.index.min(),
                "research_end": returns.index.max(),
                "research_months": len(returns),
                "strategy_sharpe": metrics["sharpe_ratio"],
                "equal_weight_sharpe": equal_weight_metrics["sharpe_ratio"],
                "static_60_40_sharpe": static_6040_metrics["sharpe_ratio"],
                "shy_sharpe": shy_metrics["sharpe_ratio"],
            }
        )
    return pd.DataFrame.from_records(records).sort_values(
        by=["passes_turnover_constraint", "selection_objective", "average_strategy_turnover"],
        ascending=[False, False, True],
    )


def select_configuration(selection_grid: pd.DataFrame) -> pd.Series:
    eligible = selection_grid[selection_grid["passes_turnover_constraint"]]
    if eligible.empty:
        eligible = selection_grid
    return eligible.sort_values(
        by=["selection_objective", "average_strategy_turnover"],
        ascending=[False, True],
    ).iloc[0]


def add_validation_benchmarks(
    returns: pd.DataFrame,
    next_returns: pd.DataFrame,
    *,
    cost_bps: float,
    fallback_asset: str,
) -> pd.DataFrame:
    static_6040 = static_spy_tlt_6040_returns(next_returns, cost_bps=cost_bps)
    shy = defensive_asset_returns(next_returns, asset=fallback_asset)
    return returns.join(static_6040, how="left").join(shy, how="left")


def defensive_asset_returns(next_returns: pd.DataFrame, *, asset: str = "SHY") -> pd.Series:
    if asset not in next_returns.columns:
        raise ValueError(f"Missing defensive benchmark asset: {asset}")
    return next_returns[asset].fillna(0.0).rename("shy_return_net")


def rolling_panel_sharpe_difference(
    returns: pd.DataFrame,
    *,
    window_months: int,
) -> pd.DataFrame:
    rows = []
    for end_position in range(window_months, len(returns) + 1):
        window = returns.iloc[end_position - window_months : end_position]
        strategy_sharpe = calculate_metrics(
            window["strategy_return_net"],
            periods_per_year=MONTHS_PER_YEAR,
        )["sharpe_ratio"]
        benchmark_sharpes = {
            "equal_weight": calculate_metrics(
                window["equal_weight_return_net"],
                periods_per_year=MONTHS_PER_YEAR,
            )["sharpe_ratio"],
            "static_60_40": calculate_metrics(
                window["static_60_40_return_net"],
                periods_per_year=MONTHS_PER_YEAR,
            )["sharpe_ratio"],
            "shy": calculate_metrics(
                window["shy_return_net"],
                periods_per_year=MONTHS_PER_YEAR,
            )["sharpe_ratio"],
        }
        best_benchmark = max(benchmark_sharpes, key=benchmark_sharpes.get)
        rows.append(
            {
                "start": window.index.min(),
                "end": window.index.max(),
                "strategy_sharpe": strategy_sharpe,
                "best_benchmark": best_benchmark,
                "best_benchmark_sharpe": benchmark_sharpes[best_benchmark],
                "strategy_minus_best_benchmark_sharpe": strategy_sharpe
                - benchmark_sharpes[best_benchmark],
            }
        )
    return pd.DataFrame.from_records(rows)


def summarize_validation_metrics(returns: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for strategy_name, column in [
        ("regime_diagnostic_net", "strategy_return_net"),
        ("equal_weight_net", "equal_weight_return_net"),
        ("static_60_40_net", "static_60_40_return_net"),
        ("shy_net", "shy_return_net"),
    ]:
        metrics = calculate_metrics(returns[column], periods_per_year=MONTHS_PER_YEAR)
        row = {"strategy": strategy_name, **metrics}
        if strategy_name == "regime_diagnostic_net":
            row["average_monthly_turnover"] = returns["strategy_turnover"].mean()
        elif strategy_name == "equal_weight_net":
            row["average_monthly_turnover"] = returns["equal_weight_turnover"].mean()
        else:
            row["average_monthly_turnover"] = pd.NA
        rows.append(row)
    return pd.DataFrame.from_records(rows)


def summarize_validation_calendar_years(returns: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for year, year_returns in returns.groupby(returns.index.year):
        row = {
            "period": str(year),
            "start": year_returns.index.min(),
            "end": year_returns.index.max(),
            "months": len(year_returns),
        }
        for name, column in [
            ("strategy", "strategy_return_net"),
            ("equal_weight", "equal_weight_return_net"),
            ("static_60_40", "static_60_40_return_net"),
            ("shy", "shy_return_net"),
        ]:
            row[f"{name}_return"] = compound_return(year_returns[column])
        row["strategy_minus_equal_weight"] = row["strategy_return"] - row["equal_weight_return"]
        row["strategy_minus_static_60_40"] = row["strategy_return"] - row["static_60_40_return"]
        row["strategy_minus_shy"] = row["strategy_return"] - row["shy_return"]
        rows.append(row)
    return pd.DataFrame.from_records(rows)


def summarize_validation_stress_periods(returns: pd.DataFrame) -> pd.DataFrame:
    periods = {
        "inflation_hiking_cycle": ("2022-01-31", "2023-12-31"),
        "recent_sample": ("2024-01-31", "2026-03-31"),
    }
    rows = []
    for period, (start, end) in periods.items():
        period_returns = returns.loc[start:end]
        if period_returns.empty:
            continue
        row = {
            "period": period,
            "start": period_returns.index.min(),
            "end": period_returns.index.max(),
            "months": len(period_returns),
        }
        for name, column in [
            ("strategy", "strategy_return_net"),
            ("equal_weight", "equal_weight_return_net"),
            ("static_60_40", "static_60_40_return_net"),
            ("shy", "shy_return_net"),
        ]:
            row[f"{name}_return"] = compound_return(period_returns[column])
            row[f"{name}_max_drawdown"] = max_drawdown(period_returns[column])
        rows.append(row)
    return pd.DataFrame.from_records(rows)


def validation_bootstrap_checks(returns: pd.DataFrame) -> pd.DataFrame:
    frames = []
    for benchmark_column in [
        "equal_weight_return_net",
        "static_60_40_return_net",
        "shy_return_net",
    ]:
        frames.append(
            bootstrap_sharpe_difference(
                returns,
                strategy_column="strategy_return_net",
                benchmark_column=benchmark_column,
                block_months=6,
                samples=1000,
                seed=17,
            )
        )
    return pd.concat(frames, ignore_index=True)


def validation_interpretation(metrics: pd.DataFrame) -> str:
    metric_by_strategy = metrics.set_index("strategy")
    strategy = metric_by_strategy.loc["regime_diagnostic_net"]
    equal_weight = metric_by_strategy.loc["equal_weight_net"]
    static_6040 = metric_by_strategy.loc["static_60_40_net"]
    shy = metric_by_strategy.loc["shy_net"]
    benchmark_sharpes = [
        equal_weight["sharpe_ratio"],
        static_6040["sharpe_ratio"],
        shy["sharpe_ratio"],
    ]
    worst_benchmark_drawdown = min(
        equal_weight["max_drawdown"],
        static_6040["max_drawdown"],
        shy["max_drawdown"],
    )
    if (
        strategy["sharpe_ratio"] > max(benchmark_sharpes)
        and strategy["max_drawdown"] >= worst_benchmark_drawdown
    ):
        return "passed_benchmark_panel"
    if strategy["sharpe_ratio"] > equal_weight["sharpe_ratio"]:
        return "beats_equal_weight_only"
    return "rejected_current_diagnostic"
