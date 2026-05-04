from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from macro_regime_portfolio_lab.backtest import MONTHS_PER_YEAR, calculate_metrics
from macro_regime_portfolio_lab.features import latest_complete_month_end, to_month_end


@dataclass(frozen=True)
class WalkForwardResult:
    returns: pd.DataFrame
    weights: pd.DataFrame
    metrics: dict[str, dict[str, float]]
    regime_counts: dict[str, int]


def build_next_month_returns(prices: pd.DataFrame) -> pd.DataFrame:
    monthly_prices = to_month_end(prices)
    monthly_prices = monthly_prices.loc[
        monthly_prices.index <= latest_complete_month_end(prices.index)
    ]
    next_returns = monthly_prices.pct_change(fill_method=None).shift(-1)
    next_returns.index.name = "date"
    return next_returns.dropna(how="all")


def align_features_and_next_returns(
    features: pd.DataFrame,
    next_returns: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    common_index = features.index.intersection(next_returns.index).sort_values()
    aligned_features = features.loc[common_index].copy()
    aligned_returns = next_returns.loc[common_index].copy()
    return aligned_features, aligned_returns


def run_regime_walk_forward(
    features: pd.DataFrame,
    next_returns: pd.DataFrame,
    *,
    min_regime_history: int = 24,
    top_n: int = 3,
    fallback_asset: str = "SHY",
) -> WalkForwardResult:
    aligned_features, aligned_returns = align_features_and_next_returns(features, next_returns)
    asset_columns = list(aligned_returns.columns)
    records = []
    weights = []

    for signal_date in aligned_features.index:
        regime = str(aligned_features.loc[signal_date, "regime"])
        history_mask = (aligned_features.index < signal_date) & (
            aligned_features["regime"] == regime
        )
        history_dates = aligned_features.index[history_mask]
        selected_assets = select_assets_from_history(
            aligned_returns.loc[history_dates],
            asset_columns,
            min_history=min_regime_history,
            top_n=top_n,
            fallback_asset=fallback_asset,
        )
        weight = equal_weight(selected_assets, asset_columns)
        realized_returns = aligned_returns.loc[signal_date].fillna(0.0)
        strategy_return = float((weight * realized_returns).sum())
        benchmark_weight = equal_weight(
            [asset for asset in asset_columns if pd.notna(aligned_returns.loc[signal_date, asset])],
            asset_columns,
        )
        benchmark_return = float((benchmark_weight * realized_returns).sum())

        records.append(
            {
                "date": signal_date,
                "regime": regime,
                "strategy_return": strategy_return,
                "equal_weight_return": benchmark_return,
                "training_observations": len(history_dates),
                "selected_assets": ",".join(selected_assets),
            }
        )
        weights.append(pd.Series(weight, name=signal_date))

    returns = pd.DataFrame.from_records(records).set_index("date")
    weight_frame = pd.DataFrame(weights)
    weight_frame.index.name = "date"
    metrics = {
        "regime_diagnostic": calculate_metrics(
            returns["strategy_return"],
            periods_per_year=MONTHS_PER_YEAR,
        ),
        "equal_weight": calculate_metrics(
            returns["equal_weight_return"],
            periods_per_year=MONTHS_PER_YEAR,
        ),
    }
    return WalkForwardResult(
        returns=returns,
        weights=weight_frame,
        metrics=metrics,
        regime_counts=returns["regime"].value_counts().sort_index().to_dict(),
    )


def select_assets_from_history(
    historical_returns: pd.DataFrame,
    asset_columns: list[str],
    *,
    min_history: int,
    top_n: int,
    fallback_asset: str,
) -> list[str]:
    if len(historical_returns) < min_history:
        return asset_columns

    average_returns = (
        historical_returns.mean(numeric_only=True).dropna().sort_values(ascending=False)
    )
    positive_assets = average_returns[average_returns > 0].head(top_n).index.tolist()
    if positive_assets:
        return positive_assets
    if fallback_asset in asset_columns:
        return [fallback_asset]
    return average_returns.head(top_n).index.tolist()


def equal_weight(selected_assets: list[str], asset_columns: list[str]) -> pd.Series:
    weight = pd.Series(0.0, index=asset_columns)
    valid_assets = [asset for asset in selected_assets if asset in asset_columns]
    if not valid_assets:
        return weight
    weight.loc[valid_assets] = 1.0 / len(valid_assets)
    return weight
