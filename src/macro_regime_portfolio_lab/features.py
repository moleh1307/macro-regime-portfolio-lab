from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from macro_regime_portfolio_lab.config import DATA_DIR, load_regime_feature_config
from macro_regime_portfolio_lab.data import write_dataset_with_manifest


def read_cached_prices(
    path: Path = DATA_DIR / "raw" / "yfinance" / "adjusted_prices.csv",
) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing {path}. Run `uv run python scripts/fetch_data.py` first.")
    return pd.read_csv(path, index_col="date", parse_dates=True).sort_index()


def read_cached_macro(path: Path = DATA_DIR / "raw" / "fred" / "macro_series.csv") -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing {path}. Run `uv run python scripts/fetch_data.py` first.")
    return pd.read_csv(path, index_col="date", parse_dates=True).sort_index()


def to_month_end(frame: pd.DataFrame) -> pd.DataFrame:
    monthly = frame.sort_index().resample("ME").last()
    monthly.index.name = "date"
    return monthly


def latest_complete_month_end(*indexes: pd.DatetimeIndex) -> pd.Timestamp:
    cutoffs = []
    for index in indexes:
        latest_observation = index.max().normalize()
        current_month_end = latest_observation + pd.offsets.MonthEnd(0)
        if latest_observation >= current_month_end:
            cutoffs.append(current_month_end)
        else:
            cutoffs.append(latest_observation - pd.offsets.MonthEnd(1))
    return min(cutoffs)


def trailing_percentile_rank(values: pd.Series, window: int) -> pd.Series:
    return values.rolling(window=window, min_periods=window).apply(
        lambda sample: pd.Series(sample).rank(pct=True).iloc[-1],
        raw=False,
    )


def build_monthly_features(
    prices: pd.DataFrame,
    macro: pd.DataFrame,
    config: dict[str, Any] | None = None,
) -> pd.DataFrame:
    regime_config = config or load_regime_feature_config()
    macro_lag_months = int(regime_config["monthly_features"]["conservative_macro_lag_months"])

    monthly_prices = to_month_end(prices)
    monthly_macro = to_month_end(macro).ffill()

    features = pd.DataFrame(index=monthly_prices.index.union(monthly_macro.index).sort_values())

    spy = monthly_prices["SPY"]
    spy_10m_average = spy.rolling(window=10, min_periods=10).mean()
    features["spy_10m_trend"] = (spy > spy_10m_average).where(spy_10m_average.notna())
    features["vix_3m_rank"] = trailing_percentile_rank(
        monthly_macro["cboe_vix"],
        window=3,
    )

    cpi_yoy_raw = monthly_macro["cpi_all_urban_consumers"].pct_change(12) * 100.0
    macro_features = pd.DataFrame(index=monthly_macro.index)
    macro_features["cpi_yoy"] = cpi_yoy_raw
    macro_features["cpi_yoy_3m_change"] = cpi_yoy_raw - cpi_yoy_raw.shift(3)
    macro_features["unemployment_3m_change"] = monthly_macro["unemployment_rate"].diff(3)
    macro_features["yield_curve_level"] = monthly_macro["ten_year_two_year_treasury_spread"]
    macro_features["yield_curve_3m_change"] = monthly_macro[
        "ten_year_two_year_treasury_spread"
    ].diff(3)
    macro_features["fed_funds_3m_change"] = monthly_macro["effective_federal_funds_rate"].diff(3)

    lagged_macro_features = macro_features.shift(macro_lag_months)
    features = features.join(lagged_macro_features, how="left")

    numeric_feature_columns = [
        "spy_10m_trend",
        "vix_3m_rank",
        "cpi_yoy",
        "cpi_yoy_3m_change",
        "unemployment_3m_change",
        "yield_curve_level",
        "yield_curve_3m_change",
        "fed_funds_3m_change",
    ]
    features = features.dropna(subset=numeric_feature_columns)
    features["spy_10m_trend"] = features["spy_10m_trend"].astype(int)

    features["growth_regime"] = classify_growth_regime(
        features["unemployment_3m_change"],
        features["spy_10m_trend"],
    )
    features["inflation_regime"] = classify_inflation_regime(features["cpi_yoy_3m_change"])
    features["regime"] = features["growth_regime"] + "_" + features["inflation_regime"]

    feature_columns = [
        "spy_10m_trend",
        "vix_3m_rank",
        "cpi_yoy",
        "cpi_yoy_3m_change",
        "unemployment_3m_change",
        "yield_curve_level",
        "yield_curve_3m_change",
        "fed_funds_3m_change",
        "growth_regime",
        "inflation_regime",
        "regime",
    ]
    features = features[feature_columns]
    features = features.loc[features.index <= latest_complete_month_end(prices.index, macro.index)]
    features.index.name = "date"
    return features


def classify_growth_regime(unemployment_change: pd.Series, spy_trend: pd.Series) -> pd.Series:
    improving_votes = (unemployment_change <= 0).astype(int) + (spy_trend == 1).astype(int)
    return pd.Series(
        ["improving_growth" if votes >= 1 else "weakening_growth" for votes in improving_votes],
        index=unemployment_change.index,
        dtype="string",
    )


def classify_inflation_regime(cpi_yoy_change: pd.Series) -> pd.Series:
    return pd.Series(
        [
            "easing_inflation" if value <= 0 else "rising_inflation"
            for value in cpi_yoy_change
        ],
        index=cpi_yoy_change.index,
        dtype="string",
    )


def build_processed_feature_cache() -> dict[str, Path]:
    prices = read_cached_prices()
    macro = read_cached_macro()
    regime_config = load_regime_feature_config()
    features = build_monthly_features(prices, macro, regime_config)

    feature_path = DATA_DIR / "processed" / "monthly_features.csv"
    manifest_path = DATA_DIR / "processed" / "monthly_features_manifest.json"
    write_dataset_with_manifest(
        features,
        feature_path,
        manifest_path,
        {
            "inputs": {
                "prices": str(DATA_DIR / "raw" / "yfinance" / "adjusted_prices.csv"),
                "macro": str(DATA_DIR / "raw" / "fred" / "macro_series.csv"),
            },
            "config": regime_config,
            "point_in_time_rule": (
                "Monthly FRED values are forward-filled after month-end resampling to use the "
                "latest available public observation. "
                "Monthly macro-derived features are shifted by "
                f"{regime_config['monthly_features']['conservative_macro_lag_months']} "
                "calendar month(s). Month-end market features are intended for allocations "
                "starting after that month-end."
            ),
        },
    )
    return {
        "features": feature_path,
        "features_manifest": manifest_path,
    }
