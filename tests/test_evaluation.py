import pandas as pd
import pytest

from macro_regime_portfolio_lab.evaluation import (
    align_features_and_next_returns,
    apply_switch_buffer,
    build_next_month_returns,
    calculate_turnover,
    rank_assets_by_risk_adjusted_history,
    run_regime_walk_forward,
    turnover_cost,
)


def test_next_month_returns_are_indexed_by_signal_month() -> None:
    prices = pd.DataFrame(
        {"SPY": [100.0, 110.0, 99.0]},
        index=pd.to_datetime(["2020-01-31", "2020-02-29", "2020-03-31"]),
    )

    returns = build_next_month_returns(prices)

    assert returns.loc[pd.Timestamp("2020-01-31"), "SPY"] == pytest.approx(0.10)
    assert returns.loc[pd.Timestamp("2020-02-29"), "SPY"] == pytest.approx(-0.10)
    assert pd.Timestamp("2020-03-31") not in returns.index


def test_next_month_returns_drop_partial_target_month() -> None:
    prices = pd.DataFrame(
        {"SPY": [100.0, 110.0, 121.0]},
        index=pd.to_datetime(["2020-01-31", "2020-02-29", "2020-03-03"]),
    )

    returns = build_next_month_returns(prices)

    assert list(returns.index) == [pd.Timestamp("2020-01-31")]


def test_alignment_keeps_only_shared_signal_dates() -> None:
    dates = pd.date_range("2020-01-31", periods=3, freq="ME")
    features = pd.DataFrame({"regime": ["a", "a", "b"]}, index=dates)
    next_returns = pd.DataFrame({"SPY": [0.1, 0.2]}, index=dates[:2])

    aligned_features, aligned_returns = align_features_and_next_returns(
        features,
        next_returns,
    )

    assert list(aligned_features.index) == list(dates[:2])
    assert list(aligned_returns.index) == list(dates[:2])


def test_walk_forward_training_excludes_current_signal_row() -> None:
    dates = pd.date_range("2020-01-31", periods=4, freq="ME")
    features = pd.DataFrame(
        {"regime": ["same", "same", "same", "same"]},
        index=dates,
    )
    next_returns = pd.DataFrame(
        {
            "SPY": [0.10, 0.10, 0.10, -0.50],
            "TLT": [-0.10, -0.10, -0.10, 0.50],
        },
        index=dates,
    )

    result = run_regime_walk_forward(
        features,
        next_returns,
        min_regime_history=1,
        top_n=1,
        fallback_asset="TLT",
    )

    # At the final signal, current-row TLT outperformance is not available to training.
    assert result.returns.loc[dates[-1], "selected_assets"] == "SPY"
    assert result.weights.loc[dates[-1], "SPY"] == 1.0
    assert result.weights.loc[dates[-1], "TLT"] == 0.0


def test_risk_adjusted_ranking_penalizes_high_volatility_assets() -> None:
    historical_returns = pd.DataFrame(
        {
            "SMOOTH": [0.01, 0.011, 0.012, 0.01],
            "JUMPY": [0.05, -0.04, 0.06, -0.03],
        }
    )

    scores = rank_assets_by_risk_adjusted_history(historical_returns)

    assert scores.index[0] == "SMOOTH"


def test_turnover_and_cost_are_half_l1_weight_change() -> None:
    previous = pd.Series({"SPY": 0.5, "TLT": 0.5})
    current = pd.Series({"SPY": 1.0, "TLT": 0.0})

    turnover = calculate_turnover(previous, current)

    assert turnover == pytest.approx(0.5)
    assert turnover_cost(turnover, cost_bps=10.0) == pytest.approx(0.0005)


def test_walk_forward_records_net_returns_after_turnover_costs() -> None:
    dates = pd.date_range("2020-01-31", periods=3, freq="ME")
    features = pd.DataFrame({"regime": ["same", "same", "same"]}, index=dates)
    next_returns = pd.DataFrame(
        {"SPY": [0.01, 0.02, 0.03], "TLT": [0.01, 0.01, 0.01]},
        index=dates,
    )

    result = run_regime_walk_forward(
        features,
        next_returns,
        min_regime_history=1,
        top_n=1,
        cost_bps=10.0,
    )

    assert "strategy_return_net" in result.returns.columns
    assert "equal_weight_return_net" in result.returns.columns
    assert result.returns["strategy_return_net"].le(result.returns["strategy_return"]).all()


def test_switch_buffer_keeps_previous_assets_without_enough_score_improvement() -> None:
    historical_returns = pd.DataFrame(
        {
            "SPY": [0.01, 0.01, 0.01, 0.02],
            "QQQ": [0.011, 0.011, 0.011, 0.02],
            "TLT": [0.012, 0.012, 0.012, 0.02],
        }
    )

    selected = apply_switch_buffer(
        previous_assets=["SPY"],
        candidate_assets=["QQQ"],
        historical_returns=historical_returns,
        buffer=0.50,
    )

    assert selected == ["SPY"]


def test_switch_buffer_accepts_large_score_improvement() -> None:
    historical_returns = pd.DataFrame(
        {
            "SPY": [0.01, -0.01, 0.01, -0.01],
            "QQQ": [0.02, 0.02, 0.02, 0.03],
        }
    )

    selected = apply_switch_buffer(
        previous_assets=["SPY"],
        candidate_assets=["QQQ"],
        historical_returns=historical_returns,
        buffer=0.10,
    )

    assert selected == ["QQQ"]
