import pandas as pd

from macro_regime_portfolio_lab.features import (
    build_monthly_features,
    classify_growth_regime,
    latest_complete_month_end,
    to_month_end,
)


def test_to_month_end_uses_last_observation_in_month() -> None:
    frame = pd.DataFrame(
        {"value": [1.0, 2.0, 3.0]},
        index=pd.to_datetime(["2020-01-02", "2020-01-31", "2020-02-03"]),
    )

    monthly = to_month_end(frame)

    assert monthly.loc[pd.Timestamp("2020-01-31"), "value"] == 2.0
    assert monthly.loc[pd.Timestamp("2020-02-29"), "value"] == 3.0


def test_monthly_features_lag_macro_but_not_market_trend() -> None:
    dates = pd.date_range("2019-01-31", periods=24, freq="ME")
    prices = pd.DataFrame({"SPY": range(100, 124)}, index=dates)
    macro = pd.DataFrame(
        {
            "cpi_all_urban_consumers": range(200, 224),
            "unemployment_rate": [4.0, 4.1, 4.2, 4.3, 4.2, 4.1] * 4,
            "ten_year_two_year_treasury_spread": [0.5, 0.4, 0.3, 0.2, 0.3, 0.4] * 4,
            "effective_federal_funds_rate": [1.0, 1.1, 1.2, 1.1, 1.0, 0.9] * 4,
            "cboe_vix": [20.0, 21.0, 22.0, 19.0, 18.0, 17.0] * 4,
        },
        index=dates,
    )
    config = {"monthly_features": {"conservative_macro_lag_months": 1}}

    features = build_monthly_features(prices, macro, config)

    observation_date = pd.Timestamp("2020-06-30")
    raw_cpi_yoy = macro["cpi_all_urban_consumers"].pct_change(12) * 100.0
    expected_lagged_cpi_yoy = raw_cpi_yoy.loc[pd.Timestamp("2020-05-31")]

    assert features.loc[observation_date, "cpi_yoy"] == expected_lagged_cpi_yoy
    assert features.loc[observation_date, "spy_10m_trend"] == 1
    assert features.loc[observation_date, "regime"] in {
        "improving_growth_easing_inflation",
        "improving_growth_rising_inflation",
        "weakening_growth_easing_inflation",
        "weakening_growth_rising_inflation",
    }


def test_monthly_features_forward_fill_macro_before_lagging() -> None:
    dates = pd.date_range("2019-01-31", periods=24, freq="ME")
    prices = pd.DataFrame({"SPY": range(100, 124)}, index=dates)
    unemployment = pd.Series([4.0, 4.1, 4.2, 4.3, 4.2, 4.1] * 4, index=dates)
    unemployment.loc[pd.Timestamp("2020-05-31")] = pd.NA
    macro = pd.DataFrame(
        {
            "cpi_all_urban_consumers": range(200, 224),
            "unemployment_rate": unemployment,
            "ten_year_two_year_treasury_spread": [0.5, 0.4, 0.3, 0.2, 0.3, 0.4] * 4,
            "effective_federal_funds_rate": [1.0, 1.1, 1.2, 1.1, 1.0, 0.9] * 4,
            "cboe_vix": [20.0, 21.0, 22.0, 19.0, 18.0, 17.0] * 4,
        },
        index=dates,
    )
    config = {"monthly_features": {"conservative_macro_lag_months": 1}}

    features = build_monthly_features(prices, macro, config)

    assert pd.Timestamp("2020-06-30") in features.index
    assert pd.notna(features.loc[pd.Timestamp("2020-06-30"), "unemployment_3m_change"])


def test_growth_regime_requires_labor_and_market_confirmation() -> None:
    dates = pd.date_range("2021-01-31", periods=4, freq="ME")
    unemployment_change = pd.Series([-0.1, -0.1, 0.2, 0.2], index=dates)
    spy_trend = pd.Series([1, 0, 1, 0], index=dates)

    growth_regime = classify_growth_regime(unemployment_change, spy_trend)

    assert growth_regime.to_list() == [
        "improving_growth",
        "weakening_growth",
        "weakening_growth",
        "weakening_growth",
    ]


def test_latest_complete_month_end_drops_partial_current_month() -> None:
    price_dates = pd.DatetimeIndex(pd.to_datetime(["2026-04-30", "2026-05-04"]))
    macro_dates = pd.DatetimeIndex(pd.to_datetime(["2026-04-30", "2026-05-01"]))

    cutoff = latest_complete_month_end(price_dates, macro_dates)

    assert cutoff == pd.Timestamp("2026-04-30")
