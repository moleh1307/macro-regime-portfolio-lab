from __future__ import annotations

from pathlib import Path

from macro_regime_portfolio_lab.backtest import BacktestResult


def write_baseline_report(result: BacktestResult, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_rows = "\n".join(
        f"| {name.replace('_', ' ').title()} | {value:.4f} |"
        for name, value in result.metrics.items()
    )
    content = f"""# Baseline Equal-Weight ETF Backtest

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
{metrics_rows}

## Caveats

- This is a framework baseline, not an investment recommendation.
- It does not include transaction costs, slippage, taxes, or borrow constraints.
- Public data can revise or backfill; cached manifests should be inspected before comparing runs.
- Regime detection and regime-aware allocation are future milestone work.
"""
    output_path.write_text(content, encoding="utf-8")
