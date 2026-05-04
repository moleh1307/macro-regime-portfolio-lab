import pandas as pd
import pytest

from macro_regime_portfolio_lab.robustness import (
    bootstrap_sharpe_difference,
    static_spy_tlt_6040_returns,
    summarize_calendar_years,
)


def test_static_6040_returns_apply_initial_turnover_cost() -> None:
    dates = pd.date_range("2020-01-31", periods=2, freq="ME")
    next_returns = pd.DataFrame(
        {"SPY": [0.10, 0.00], "TLT": [0.00, 0.00]},
        index=dates,
    )

    returns = static_spy_tlt_6040_returns(next_returns, cost_bps=10.0)

    assert returns.iloc[0] == 0.0595
    assert returns.iloc[1] < 0.0


def test_calendar_year_summary_compounds_returns() -> None:
    dates = pd.to_datetime(["2020-01-31", "2020-02-29", "2021-01-31"])
    returns = pd.DataFrame(
        {
            "strategy_return_net": [0.10, 0.10, 0.00],
            "equal_weight_return_net": [0.05, 0.00, 0.00],
            "static_60_40_return_net": [0.00, 0.00, 0.00],
        },
        index=dates,
    )

    summary = summarize_calendar_years(returns)

    assert summary.loc[summary["period"] == "2020", "strategy_return"].iloc[0] == pytest.approx(
        0.21
    )


def test_bootstrap_sharpe_difference_is_deterministic() -> None:
    dates = pd.date_range("2020-01-31", periods=12, freq="ME")
    returns = pd.DataFrame(
        {
            "strategy": [0.02, -0.01, 0.03, 0.00] * 3,
            "benchmark": [0.01, -0.01, 0.02, 0.00] * 3,
        },
        index=dates,
    )

    first = bootstrap_sharpe_difference(
        returns,
        strategy_column="strategy",
        benchmark_column="benchmark",
        block_months=3,
        samples=25,
        seed=11,
    )
    second = bootstrap_sharpe_difference(
        returns,
        strategy_column="strategy",
        benchmark_column="benchmark",
        block_months=3,
        samples=25,
        seed=11,
    )

    pd.testing.assert_frame_equal(first, second)
