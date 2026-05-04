from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

TRADING_DAYS_PER_YEAR = 252


@dataclass(frozen=True)
class BacktestResult:
    daily_returns: pd.Series
    equity_curve: pd.Series
    weights: pd.DataFrame
    metrics: dict[str, float]


def monthly_equal_weight_returns(prices: pd.DataFrame) -> BacktestResult:
    clean_prices = prices.sort_index().dropna(how="all")
    raw_returns = clean_prices.pct_change(fill_method=None).dropna(how="all")
    asset_available = clean_prices.notna().reindex(raw_returns.index)
    returns = raw_returns
    valid_assets = returns.columns[returns.notna().any()].tolist()
    returns = returns[valid_assets].fillna(0.0)
    asset_available = asset_available[valid_assets].fillna(False)

    month_key = pd.Series(returns.index.to_period("M"), index=returns.index)
    first_day_of_month = month_key.ne(month_key.shift(1))
    weights = pd.DataFrame(0.0, index=returns.index, columns=valid_assets)

    current_weight = pd.Series(0.0, index=valid_assets)
    for date in returns.index:
        if first_day_of_month.loc[date]:
            available = asset_available.loc[date]
            if available.any():
                current_weight = pd.Series(0.0, index=valid_assets)
                current_weight.loc[available] = 1.0 / available.sum()
        weights.loc[date] = current_weight

    portfolio_returns = (weights.shift(1).fillna(0.0) * returns).sum(axis=1)
    equity_curve = (1.0 + portfolio_returns).cumprod()

    return BacktestResult(
        daily_returns=portfolio_returns,
        equity_curve=equity_curve,
        weights=weights,
        metrics=calculate_metrics(portfolio_returns),
    )


def calculate_metrics(returns: pd.Series) -> dict[str, float]:
    returns = returns.dropna()
    if returns.empty:
        return {
            "annualized_return": 0.0,
            "annualized_volatility": 0.0,
            "sharpe_ratio": 0.0,
            "max_drawdown": 0.0,
        }

    equity = (1.0 + returns).cumprod()
    years = len(returns) / TRADING_DAYS_PER_YEAR
    annualized_return = equity.iloc[-1] ** (1.0 / years) - 1.0 if years > 0 else 0.0
    annualized_volatility = returns.std(ddof=0) * np.sqrt(TRADING_DAYS_PER_YEAR)
    sharpe_ratio = (
        annualized_return / annualized_volatility if annualized_volatility > 0 else 0.0
    )
    drawdown = equity / equity.cummax() - 1.0

    return {
        "annualized_return": float(annualized_return),
        "annualized_volatility": float(annualized_volatility),
        "sharpe_ratio": float(sharpe_ratio),
        "max_drawdown": float(drawdown.min()),
    }
