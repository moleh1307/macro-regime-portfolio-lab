# Baseline Equal-Weight ETF Backtest

## Purpose

This report verifies the first reproducible backtest path. It is not a regime-aware
strategy and should not be interpreted as an outperformance claim.

## Method

- Universe: configured ETF universe in `configs/assets.yml`.
- Data: adjusted close prices cached from Yahoo Finance via `yfinance`.
- Portfolio: equal weight across available ETFs.
- Rebalance: monthly.
- Transaction costs: not modeled in this baseline.
- Live trading/execution: out of scope.

## Metrics

| Metric | Value |
| --- | ---: |
| Annualized Return | 0.0735 |
| Annualized Volatility | 0.1147 |
| Sharpe Ratio | 0.6408 |
| Max Drawdown | -0.3240 |

## Caveats

- This is a framework baseline, not an investment recommendation.
- It does not include transaction costs, slippage, taxes, or borrow constraints.
- Public data can revise or backfill; cached manifests should be inspected before comparing runs.
- Regime detection and regime-aware allocation are future milestone work.
