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
    switch_score_buffer: float = 0.10,
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
        selected_assets = apply_switch_buffer(
            previous_assets=assets_from_weight(previous_strategy_weight),
            candidate_assets=selected_assets,
            historical_returns=aligned_returns.loc[history_dates],
            buffer=switch_score_buffer,
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
                "switch_score_buffer": switch_score_buffer,
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


def run_parameter_sensitivity_grid(
    features: pd.DataFrame,
    next_returns: pd.DataFrame,
    *,
    switch_score_buffers: list[float],
    cost_bps_values: list[float],
    min_regime_history: int = 24,
    top_n: int = 3,
    fallback_asset: str = "SHY",
) -> pd.DataFrame:
    records = []
    for switch_score_buffer in switch_score_buffers:
        for cost_bps in cost_bps_values:
            result = run_regime_walk_forward(
                features,
                next_returns,
                min_regime_history=min_regime_history,
                top_n=top_n,
                fallback_asset=fallback_asset,
                cost_bps=cost_bps,
                switch_score_buffer=switch_score_buffer,
            )
            strategy_net = result.metrics["regime_diagnostic_net"]
            equal_weight_net = result.metrics["equal_weight_net"]
            records.append(
                {
                    "switch_score_buffer": switch_score_buffer,
                    "cost_bps": cost_bps,
                    "strategy_net_annualized_return": strategy_net["annualized_return"],
                    "strategy_net_volatility": strategy_net["annualized_volatility"],
                    "strategy_net_sharpe": strategy_net["sharpe_ratio"],
                    "strategy_net_max_drawdown": strategy_net["max_drawdown"],
                    "equal_weight_net_annualized_return": equal_weight_net[
                        "annualized_return"
                    ],
                    "equal_weight_net_volatility": equal_weight_net[
                        "annualized_volatility"
                    ],
                    "equal_weight_net_sharpe": equal_weight_net["sharpe_ratio"],
                    "equal_weight_net_max_drawdown": equal_weight_net["max_drawdown"],
                    "average_strategy_turnover": result.returns[
                        "strategy_turnover"
                    ].mean(),
                    "average_equal_weight_turnover": result.returns[
                        "equal_weight_turnover"
                    ].mean(),
                    "months": len(result.returns),
                }
            )
    return pd.DataFrame.from_records(records)


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


def apply_switch_buffer(
    previous_assets: list[str],
    candidate_assets: list[str],
    historical_returns: pd.DataFrame,
    *,
    buffer: float,
) -> list[str]:
    if not previous_assets or set(previous_assets) == set(candidate_assets):
        return candidate_assets
    previous_score = basket_score(previous_assets, historical_returns)
    candidate_score = basket_score(candidate_assets, historical_returns)
    if pd.isna(previous_score) or pd.isna(candidate_score):
        return candidate_assets
    if candidate_score > previous_score * (1.0 + buffer):
        return candidate_assets
    return previous_assets


def basket_score(assets: list[str], historical_returns: pd.DataFrame) -> float:
    valid_assets = [asset for asset in assets if asset in historical_returns.columns]
    if not valid_assets or historical_returns.empty:
        return float("nan")
    basket_returns = historical_returns[valid_assets].mean(axis=1)
    volatility = basket_returns.std(ddof=0)
    if volatility == 0 or pd.isna(volatility):
        return float("nan")
    return float(basket_returns.mean() / volatility)


def assets_from_weight(weight: pd.Series) -> list[str]:
    return weight[weight > 0].index.tolist()


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
