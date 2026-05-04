import pandas as pd

from macro_regime_portfolio_lab.validation import (
    ValidationConfig,
    build_selection_grid,
    parse_validation_config,
    split_research_validation,
)


def test_parse_validation_config_sets_locked_split() -> None:
    config = parse_validation_config(
        {
            "split": {
                "research_start": "2008-05-31",
                "research_end": "2021-12-31",
                "validation_start": "2022-01-31",
            },
            "selection": {
                "rolling_window_months": 36,
                "max_average_monthly_turnover": 0.12,
                "cost_bps": 5.0,
                "fallback_asset": "SHY",
                "switch_score_buffers": [0.0, 0.1],
                "min_regime_history_values": [12, 24],
                "top_n_values": [2, 3],
            },
        }
    )

    assert config.research_end == pd.Timestamp("2021-12-31")
    assert config.validation_start == pd.Timestamp("2022-01-31")


def test_split_research_validation_excludes_validation_from_research() -> None:
    dates = pd.date_range("2021-10-31", periods=5, freq="ME")
    features = pd.DataFrame({"regime": ["same"] * 5}, index=dates)
    next_returns = pd.DataFrame({"SPY": [0.01] * 5}, index=dates)
    config = validation_config_for_tests()

    research_features, research_returns, validation_features, validation_returns = (
        split_research_validation(features, next_returns, config)
    )

    assert research_features.index.max() <= config.research_end
    assert research_returns.index.max() <= config.research_end
    assert validation_features.index.min() >= config.validation_start
    assert validation_returns.index.min() >= config.validation_start


def test_selection_grid_uses_only_research_rows() -> None:
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
    altered_validation_returns = next_returns.copy()
    altered_validation_returns.loc[altered_validation_returns.index >= "2022-01-31", "SPY"] = 0.99
    config = validation_config_for_tests()

    research_features, research_returns, _, _ = split_research_validation(
        features,
        next_returns,
        config,
    )
    _, altered_research_returns, _, _ = split_research_validation(
        features,
        altered_validation_returns,
        config,
    )
    original_grid = build_selection_grid(research_features, research_returns, config)
    altered_grid = build_selection_grid(research_features, altered_research_returns, config)

    assert original_grid["research_end"].max() <= config.research_end
    pd.testing.assert_frame_equal(
        original_grid.reset_index(drop=True),
        altered_grid.reset_index(drop=True),
    )


def validation_config_for_tests() -> ValidationConfig:
    return ValidationConfig(
        research_start=pd.Timestamp("2021-06-30"),
        research_end=pd.Timestamp("2021-12-31"),
        validation_start=pd.Timestamp("2022-01-31"),
        rolling_window_months=3,
        max_average_monthly_turnover=1.0,
        cost_bps=5.0,
        fallback_asset="SHY",
        switch_score_buffers=[0.0, 0.1],
        min_regime_history_values=[1],
        top_n_values=[1],
    )
