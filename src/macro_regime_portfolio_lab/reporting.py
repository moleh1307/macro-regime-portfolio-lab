from __future__ import annotations

from pathlib import Path

from macro_regime_portfolio_lab.backtest import BacktestResult
from macro_regime_portfolio_lab.evaluation import WalkForwardResult


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


def write_walk_forward_report(result: WalkForwardResult, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_rows = []
    for strategy_name, metrics in result.metrics.items():
        for metric_name, value in metrics.items():
            metrics_rows.append(
                f"| {strategy_name} | {metric_name.replace('_', ' ').title()} | {value:.4f} |"
            )
    regime_rows = "\n".join(
        f"| {regime} | {count} |" for regime, count in result.regime_counts.items()
    )
    metrics_table = "\n".join(metrics_rows)
    start = result.returns.index.min().date()
    end = result.returns.index.max().date()
    content = f"""# Walk-Forward Regime Evaluation Diagnostic

## Purpose

This report verifies the walk-forward evaluation protocol. It is a diagnostic
research scaffold, not a robustness claim, investment recommendation, or live
allocation system.

## Method

- Signal date: month end.
- Target return: next-month ETF return, aligned to the signal month.
- Training rule: each signal uses only earlier rows with the same regime label.
- Diagnostic allocation: top historical same-regime assets by average next-month
  return, equal-weighted, with equal-weight fallback until enough same-regime
  observations exist.
- Benchmark: monthly equal weight across the configured ETF universe.
- Transaction costs: not modeled.
- Evaluation period: {start} to {end}.

## Metrics

| Strategy | Metric | Value |
| --- | --- | ---: |
{metrics_table}

## Regime Counts

| Regime | Months |
| --- | ---: |
{regime_rows}

## Caveats

- This protocol is designed to catch alignment and leakage problems before
  stronger strategy research.
- The diagnostic allocation is intentionally simple and should not be treated as
  a final investment model.
- It does not include transaction costs, slippage, taxes, liquidity limits, or
  exact macro-release calendars.
- Any apparent performance difference requires further robustness checks before
  being used in public claims.
"""
    output_path.write_text(content, encoding="utf-8")
