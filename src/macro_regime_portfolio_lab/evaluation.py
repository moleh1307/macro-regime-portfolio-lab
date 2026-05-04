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
    cost_bps: float


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
    cost_bps: float = 5.0,
) -> WalkForwardResult:
    aligned_features, aligned_returns = align_features_and_next_returns(features, next_returns)
    asset_columns = list(aligned_returns.columns)
    records = []
    weights = []

    previous_strategy_weight = pd.Series(0.0, index=asset_columns)
    previous_benchmark_weight = pd.Series(0.0, index=asset_columns)

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
        strategy_turnover = calculate_turnover(previous_strategy_weight, weight)
        benchmark_turnover = calculate_turnover(previous_benchmark_weight, benchmark_weight)
        strategy_cost = turnover_cost(strategy_turnover, cost_bps)
        benchmark_cost = turnover_cost(benchmark_turnover, cost_bps)

        records.append(
            {
                "date": signal_date,
                "regime": regime,
                "strategy_return": strategy_return,
                "strategy_turnover": strategy_turnover,
                "strategy_cost": strategy_cost,
                "strategy_return_net": strategy_return - strategy_cost,
                "equal_weight_return": benchmark_return,
                "equal_weight_turnover": benchmark_turnover,
                "equal_weight_cost": benchmark_cost,
                "equal_weight_return_net": benchmark_return - benchmark_cost,
                "training_observations": len(history_dates),
                "selected_assets": ",".join(selected_assets),
            }
        )
        weights.append(pd.Series(weight, name=signal_date))
        previous_strategy_weight = weight
        previous_benchmark_weight = benchmark_weight

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
        "regime_diagnostic_net": calculate_metrics(
            returns["strategy_return_net"],
            periods_per_year=MONTHS_PER_YEAR,
        ),
        "equal_weight_net": calculate_metrics(
            returns["equal_weight_return_net"],
            periods_per_year=MONTHS_PER_YEAR,
        ),
    }
    return WalkForwardResult(
        returns=returns,
        weights=weight_frame,
        metrics=metrics,
        regime_counts=returns["regime"].value_counts().sort_index().to_dict(),
        cost_bps=cost_bps,
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

    scores = rank_assets_by_risk_adjusted_history(historical_returns)
    selected_assets = scores[scores > 0].head(top_n).index.tolist()
    if selected_assets:
        return selected_assets
    if fallback_asset in asset_columns:
        return [fallback_asset]
    return scores.head(top_n).index.tolist()


def rank_assets_by_risk_adjusted_history(historical_returns: pd.DataFrame) -> pd.Series:
    average_returns = historical_returns.mean(numeric_only=True)
    volatility = historical_returns.std(numeric_only=True, ddof=0).replace(0.0, pd.NA)
    scores = (average_returns / volatility).dropna().sort_values(ascending=False)
    return scores


def equal_weight(selected_assets: list[str], asset_columns: list[str]) -> pd.Series:
    weight = pd.Series(0.0, index=asset_columns)
    valid_assets = [asset for asset in selected_assets if asset in asset_columns]
    if not valid_assets:
        return weight
    weight.loc[valid_assets] = 1.0 / len(valid_assets)
    return weight


def calculate_turnover(previous_weight: pd.Series, current_weight: pd.Series) -> float:
    aligned_previous, aligned_current = previous_weight.align(current_weight, fill_value=0.0)
    return float((aligned_current - aligned_previous).abs().sum() / 2.0)


def turnover_cost(turnover: float, cost_bps: float) -> float:
    return float(turnover * cost_bps / 10_000.0)
