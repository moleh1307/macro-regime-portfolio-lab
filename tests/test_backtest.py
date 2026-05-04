import pandas as pd

from macro_regime_portfolio_lab.backtest import calculate_metrics, monthly_equal_weight_returns


def test_monthly_equal_weight_returns_produces_equity_curve() -> None:
    dates = pd.bdate_range("2020-01-01", periods=80)
    sequence = pd.Series(range(len(dates)))
    prices = pd.DataFrame(
        {
            "SPY": 100.0 + sequence.to_numpy(),
            "IEF": 100.0 + sequence.mul(0.25).to_numpy(),
        },
        index=dates,
    )

    result = monthly_equal_weight_returns(prices)

    assert len(result.daily_returns) == len(dates) - 1
    assert len(result.equity_curve) == len(result.daily_returns)
    assert set(result.weights.columns) == {"SPY", "IEF"}
    assert result.metrics["annualized_volatility"] >= 0


def test_calculate_metrics_handles_empty_returns() -> None:
    metrics = calculate_metrics(pd.Series(dtype=float))

    assert metrics == {
        "annualized_return": 0.0,
        "annualized_volatility": 0.0,
        "sharpe_ratio": 0.0,
        "max_drawdown": 0.0,
    }
