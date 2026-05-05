import pandas as pd
import pytest

from macro_regime_portfolio_lab.turnover_stability import (
    POST_HOLDOUT_REVIEW_LABEL,
    TurnoverStabilityConfig,
    build_turnover_stability_grid,
    calculate_turnover_stability_metrics,
    parse_turnover_stability_config,
    select_turnover_stable_candidate,
    split_research_post_holdout,
)


def test_turnover_stability_metrics_capture_clustered_turnover() -> None:
    turnover = pd.Series([0.0, 0.1, 0.5, 0.5, 0.0, 0.0])

    metrics = calculate_turnover_stability_metrics(
        turnover,
        high_turnover_threshold=0.25,
    )

    assert metrics["average_turnover"] == pytest.approx(11 / 60)
    assert metrics["high_turnover_month_share"] == pytest.approx(2 / 6)
    assert metrics["turnover_p95"] >= metrics["turnover_p90"]


def test_turnover_stability_metrics_can_exclude_warmup_turnover() -> None:
    turnover = pd.Series([0.5, 0.0, 0.0, 0.1, 0.1])

    metrics = calculate_turnover_stability_metrics(
        turnover,
        high_turnover_threshold=0.25,
        warmup_months=1,
    )

    assert metrics["rolling_12m_average_turnover_max"] == pytest.approx(0.05)
    assert metrics["high_turnover_month_share"] == 0.0


def test_turnover_stability_split_excludes_post_holdout_from_research() -> None:
    dates = pd.date_range("2021-10-31", periods=5, freq="ME")
    features = pd.DataFrame({"regime": ["same"] * 5}, index=dates)
    next_returns = pd.DataFrame({"SPY": [0.01] * 5}, index=dates)
    config = turnover_config_for_tests()

    research_features, research_returns, post_features, post_returns = (
        split_research_post_holdout(features, next_returns, config)
    )

    assert research_features.index.max() <= config.research_end
    assert research_returns.index.max() <= config.research_end
    assert post_features.index.min() >= config.post_holdout_start
    assert post_returns.index.min() >= config.post_holdout_start


def test_rejected_candidate_cannot_be_selected() -> None:
    grid = pd.DataFrame(
        {
            "selection_score": [100.0, 0.0],
            "average_turnover": [0.01, 0.02],
            "passes_turnover_stability": [False, True],
        }
    )

    selected = select_turnover_stable_candidate(grid)

    assert selected["selection_score"] == 0.0
    assert bool(selected["passes_turnover_stability"])


def test_post_holdout_review_label_is_explicit() -> None:
    assert POST_HOLDOUT_REVIEW_LABEL == "post-holdout-review diagnostic run"


def test_candidate_grid_uses_only_research_rows() -> None:
    dates = pd.date_range("2021-06-30", periods=10, freq="ME")
    features = pd.DataFrame({"regime": ["same"] * len(dates)}, index=dates)
    next_returns = pd.DataFrame(
        {
            "SPY": [0.01, 0.02, 0.01, 0.02, 0.01, 0.02, -0.99, -0.99, -0.99, -0.99],
            "TLT": [0.00] * 10,
            "SHY": [0.001] * 10,
        },
        index=dates,
    )
    altered_post_holdout = next_returns.copy()
    altered_post_holdout.loc[altered_post_holdout.index >= "2022-01-31", "SPY"] = 0.99
    config = turnover_config_for_tests()

    research_features, research_returns, _, _ = split_research_post_holdout(
        features,
        next_returns,
        config,
    )
    _, altered_research_returns, _, _ = split_research_post_holdout(
        features,
        altered_post_holdout,
        config,
    )

    original_grid = build_turnover_stability_grid(research_features, research_returns, config)
    altered_grid = build_turnover_stability_grid(
        research_features,
        altered_research_returns,
        config,
    )

    assert original_grid["research_end"].max() <= config.research_end
    pd.testing.assert_frame_equal(
        original_grid.reset_index(drop=True),
        altered_grid.reset_index(drop=True),
    )


def test_parse_turnover_stability_config() -> None:
    config = parse_turnover_stability_config(
        {
            "split": {
                "research_start": "2008-05-31",
                "research_end": "2021-12-31",
                "post_holdout_start": "2022-01-31",
            },
            "selection": {
                "rolling_window_months": 36,
                "cost_bps": 5.0,
                "fallback_asset": "SHY",
                "high_turnover_threshold": 0.25,
                "turnover_metric_warmup_months": 12,
                "hard_thresholds": {
                    "average_turnover": 0.10,
                    "turnover_p90": 0.35,
                    "turnover_p95": 0.50,
                    "high_turnover_month_share": 0.20,
                    "turnover_volatility": 0.18,
                    "rolling_12m_average_turnover_max": 0.18,
                },
                "objective_penalties": {
                    "turnover_instability": 0.50,
                    "allocation_complexity": 0.25,
                },
                "switch_score_buffers": [0.20],
                "min_regime_history_values": [12],
                "top_n_values": [2],
                "max_monthly_turnover_values": [0.15],
            },
            "report": {"label": POST_HOLDOUT_REVIEW_LABEL},
        }
    )

    assert config.post_holdout_start == pd.Timestamp("2022-01-31")
    assert config.max_monthly_turnover_values == [0.15]
    assert config.turnover_metric_warmup_months == 12


def turnover_config_for_tests() -> TurnoverStabilityConfig:
    return TurnoverStabilityConfig(
        research_start=pd.Timestamp("2021-06-30"),
        research_end=pd.Timestamp("2021-12-31"),
        post_holdout_start=pd.Timestamp("2022-01-31"),
        rolling_window_months=3,
        cost_bps=5.0,
        fallback_asset="SHY",
        high_turnover_threshold=0.25,
        turnover_metric_warmup_months=0,
        hard_thresholds={
            "average_turnover": 1.0,
            "turnover_p90": 1.0,
            "turnover_p95": 1.0,
            "high_turnover_month_share": 1.0,
            "turnover_volatility": 1.0,
            "rolling_12m_average_turnover_max": 1.0,
        },
        turnover_instability_penalty=0.50,
        allocation_complexity_penalty=0.25,
        switch_score_buffers=[0.20],
        min_regime_history_values=[1],
        top_n_values=[1],
        max_monthly_turnover_values=[0.15],
        report_label=POST_HOLDOUT_REVIEW_LABEL,
    )
