from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from macro_regime_portfolio_lab.backtest import MONTHS_PER_YEAR, calculate_metrics
from macro_regime_portfolio_lab.evaluation import (
    calculate_turnover,
    run_regime_walk_forward,
    turnover_cost,
)


@dataclass(frozen=True)
class RobustnessReview:
    full_sample: pd.DataFrame
    subperiods: pd.DataFrame
    stress_periods: pd.DataFrame
    rolling_windows: pd.DataFrame
    buffer_subperiods: pd.DataFrame
    bootstrap: pd.DataFrame


def static_spy_tlt_6040_returns(
    next_returns: pd.DataFrame,
    *,
    cost_bps: float = 5.0,
) -> pd.Series:
    required_assets = ["SPY", "TLT"]
    missing_assets = [asset for asset in required_assets if asset not in next_returns.columns]
    if missing_assets:
        raise ValueError(f"Missing required 60/40 assets: {missing_assets}")

    target_weight = pd.Series(0.0, index=next_returns.columns)
    target_weight.loc["SPY"] = 0.60
    target_weight.loc["TLT"] = 0.40
    previous_weight = pd.Series(0.0, index=next_returns.columns)
    records = []
    for date, realized_returns in next_returns.sort_index().iterrows():
        realized_returns = realized_returns.fillna(0.0)
        cost = turnover_cost(calculate_turnover(previous_weight, target_weight), cost_bps)
        portfolio_return = float((target_weight * realized_returns).sum())
        records.append((date, portfolio_return - cost))
        ending_weight = target_weight * (1.0 + realized_returns)
        ending_value = ending_weight.sum()
        previous_weight = ending_weight / ending_value if ending_value > 0 else target_weight
    return pd.Series(
        [value for _, value in records],
        index=pd.DatetimeIndex([date for date, _ in records], name="date"),
        name="static_60_40_return_net",
    )


def summarize_full_sample(returns: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for name, column in [
        ("regime_diagnostic_net", "strategy_return_net"),
        ("equal_weight_net", "equal_weight_return_net"),
        ("static_60_40_net", "static_60_40_return_net"),
    ]:
        metrics = calculate_metrics(returns[column], periods_per_year=MONTHS_PER_YEAR)
        rows.append({"strategy": name, **metrics})
    return pd.DataFrame.from_records(rows)


def summarize_calendar_years(returns: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for year, year_returns in returns.groupby(returns.index.year):
        row = {
            "period": str(year),
            "start": year_returns.index.min(),
            "end": year_returns.index.max(),
        }
        for name, column in [
            ("strategy", "strategy_return_net"),
            ("equal_weight", "equal_weight_return_net"),
            ("static_60_40", "static_60_40_return_net"),
        ]:
            row[f"{name}_return"] = compound_return(year_returns[column])
        row["strategy_minus_equal_weight"] = row["strategy_return"] - row["equal_weight_return"]
        row["strategy_minus_static_60_40"] = row["strategy_return"] - row["static_60_40_return"]
        rows.append(row)
    return pd.DataFrame.from_records(rows)


def summarize_stress_periods(returns: pd.DataFrame) -> pd.DataFrame:
    periods = {
        "gfc_available_sample": ("2008-05-31", "2009-06-30"),
        "covid_shock_recovery": ("2020-02-29", "2020-12-31"),
        "inflation_hiking_cycle": ("2022-01-31", "2023-12-31"),
        "recent_sample": ("2024-01-31", "2026-03-31"),
    }
    rows = []
    for period_name, (start, end) in periods.items():
        period_returns = returns.loc[start:end]
        if period_returns.empty:
            continue
        row = {
            "period": period_name,
            "start": period_returns.index.min(),
            "end": period_returns.index.max(),
            "months": len(period_returns),
        }
        for name, column in [
            ("strategy", "strategy_return_net"),
            ("equal_weight", "equal_weight_return_net"),
            ("static_60_40", "static_60_40_return_net"),
        ]:
            row[f"{name}_return"] = compound_return(period_returns[column])
            row[f"{name}_max_drawdown"] = max_drawdown(period_returns[column])
        row["strategy_minus_equal_weight"] = row["strategy_return"] - row["equal_weight_return"]
        row["strategy_minus_static_60_40"] = row["strategy_return"] - row["static_60_40_return"]
        rows.append(row)
    return pd.DataFrame.from_records(rows)


def summarize_rolling_windows(returns: pd.DataFrame, *, window_months: int = 36) -> pd.DataFrame:
    rows = []
    for end_position in range(window_months, len(returns) + 1):
        window = returns.iloc[end_position - window_months : end_position]
        strategy_metrics = calculate_metrics(
            window["strategy_return_net"],
            periods_per_year=MONTHS_PER_YEAR,
        )
        equal_weight_metrics = calculate_metrics(
            window["equal_weight_return_net"],
            periods_per_year=MONTHS_PER_YEAR,
        )
        static_6040_metrics = calculate_metrics(
            window["static_60_40_return_net"],
            periods_per_year=MONTHS_PER_YEAR,
        )
        rows.append(
            {
                "start": window.index.min(),
                "end": window.index.max(),
                "months": len(window),
                "strategy_sharpe": strategy_metrics["sharpe_ratio"],
                "equal_weight_sharpe": equal_weight_metrics["sharpe_ratio"],
                "static_60_40_sharpe": static_6040_metrics["sharpe_ratio"],
                "strategy_minus_equal_weight_sharpe": strategy_metrics["sharpe_ratio"]
                - equal_weight_metrics["sharpe_ratio"],
                "strategy_minus_static_60_40_sharpe": strategy_metrics["sharpe_ratio"]
                - static_6040_metrics["sharpe_ratio"],
            }
        )
    return pd.DataFrame.from_records(rows)


def summarize_buffer_subperiods(
    features: pd.DataFrame,
    next_returns: pd.DataFrame,
    *,
    switch_score_buffers: list[float],
    cost_bps: float = 5.0,
) -> pd.DataFrame:
    rows = []
    static_6040 = static_spy_tlt_6040_returns(next_returns, cost_bps=cost_bps)
    for buffer in switch_score_buffers:
        result = run_regime_walk_forward(
            features,
            next_returns,
            cost_bps=cost_bps,
            switch_score_buffer=buffer,
        )
        returns = result.returns.join(static_6040, how="left")
        for year, year_returns in returns.groupby(returns.index.year):
            strategy_return = compound_return(year_returns["strategy_return_net"])
            equal_return = compound_return(year_returns["equal_weight_return_net"])
            static_return = compound_return(year_returns["static_60_40_return_net"])
            rows.append(
                {
                    "switch_score_buffer": buffer,
                    "period": str(year),
                    "months": len(year_returns),
                    "strategy_return": strategy_return,
                    "equal_weight_return": equal_return,
                    "static_60_40_return": static_return,
                    "strategy_minus_equal_weight": strategy_return - equal_return,
                    "strategy_minus_static_60_40": strategy_return - static_return,
                    "average_strategy_turnover": year_returns["strategy_turnover"].mean(),
                }
            )
    return pd.DataFrame.from_records(rows)


def bootstrap_sharpe_difference(
    returns: pd.DataFrame,
    *,
    strategy_column: str,
    benchmark_column: str,
    block_months: int = 6,
    samples: int = 1000,
    seed: int = 7,
) -> pd.DataFrame:
    paired = returns[[strategy_column, benchmark_column]].dropna()
    rng = np.random.default_rng(seed)
    differences = []
    max_start = max(len(paired) - block_months, 0)
    for _ in range(samples):
        sampled_positions = []
        while len(sampled_positions) < len(paired):
            start = int(rng.integers(0, max_start + 1))
            sampled_positions.extend(range(start, start + block_months))
        sampled_positions = sampled_positions[: len(paired)]
        sample = paired.iloc[sampled_positions]
        strategy_sharpe = calculate_metrics(
            sample[strategy_column],
            periods_per_year=MONTHS_PER_YEAR,
        )["sharpe_ratio"]
        benchmark_sharpe = calculate_metrics(
            sample[benchmark_column],
            periods_per_year=MONTHS_PER_YEAR,
        )["sharpe_ratio"]
        differences.append(strategy_sharpe - benchmark_sharpe)

    difference_series = pd.Series(differences)
    observed = (
        calculate_metrics(paired[strategy_column], periods_per_year=MONTHS_PER_YEAR)[
            "sharpe_ratio"
        ]
        - calculate_metrics(paired[benchmark_column], periods_per_year=MONTHS_PER_YEAR)[
            "sharpe_ratio"
        ]
    )
    return pd.DataFrame.from_records(
        [
            {
                "strategy_column": strategy_column,
                "benchmark_column": benchmark_column,
                "observed_sharpe_difference": observed,
                "bootstrap_mean_difference": difference_series.mean(),
                "bootstrap_p05": difference_series.quantile(0.05),
                "bootstrap_p50": difference_series.quantile(0.50),
                "bootstrap_p95": difference_series.quantile(0.95),
                "share_positive": float((difference_series > 0).mean()),
                "block_months": block_months,
                "samples": samples,
                "seed": seed,
            }
        ]
    )


def run_robustness_review(
    features: pd.DataFrame,
    next_returns: pd.DataFrame,
    *,
    cost_bps: float = 5.0,
) -> RobustnessReview:
    result = run_regime_walk_forward(features, next_returns, cost_bps=cost_bps)
    static_6040 = static_spy_tlt_6040_returns(next_returns, cost_bps=cost_bps)
    returns = result.returns.join(static_6040, how="left")
    bootstrap = pd.concat(
        [
            bootstrap_sharpe_difference(
                returns,
                strategy_column="strategy_return_net",
                benchmark_column="equal_weight_return_net",
            ),
            bootstrap_sharpe_difference(
                returns,
                strategy_column="strategy_return_net",
                benchmark_column="static_60_40_return_net",
            ),
        ],
        ignore_index=True,
    )
    return RobustnessReview(
        full_sample=summarize_full_sample(returns),
        subperiods=summarize_calendar_years(returns),
        stress_periods=summarize_stress_periods(returns),
        rolling_windows=summarize_rolling_windows(returns),
        buffer_subperiods=summarize_buffer_subperiods(
            features,
            next_returns,
            switch_score_buffers=[0.10, 0.20, 0.50],
            cost_bps=cost_bps,
        ),
        bootstrap=bootstrap,
    )


def compound_return(returns: pd.Series) -> float:
    clean_returns = returns.dropna()
    if clean_returns.empty:
        return 0.0
    return float((1.0 + clean_returns).prod() - 1.0)


def max_drawdown(returns: pd.Series) -> float:
    clean_returns = returns.dropna()
    if clean_returns.empty:
        return 0.0
    equity = (1.0 + clean_returns).cumprod()
    drawdown = equity / equity.cummax() - 1.0
    return float(drawdown.min())
