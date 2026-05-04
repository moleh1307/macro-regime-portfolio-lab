# MRPL-002 - Run First Public-Data Fetch And Baseline Report

- Owner role: Data Engineer / Quant Researcher
- Status: done
- Lifecycle state: Done
- Risk lane: normal
- Canonical artifact: `artifacts/reports/baseline_equal_weight.md`

## Scope

Run the milestone 1 workflow end to end:

- Sync dependencies.
- Fetch ETF adjusted close prices from `yfinance`.
- Fetch configured FRED macro series.
- Write cached raw datasets and source manifests.
- Run the monthly equal-weight baseline backtest.
- Generate the baseline markdown report.

## Acceptance Criteria

- Data manifests exist for prices and macro data.
- Manifest row counts, date ranges, and columns are plausible.
- Baseline report exists and states that it is not an outperformance claim.
- Metrics are produced without runtime errors.

## Verification Evidence

- `uv run python scripts/fetch_data.py` completed.
- yfinance prices manifest: 4,864 rows, 12 ETF columns, 2007-01-03 to 2026-05-04.
- FRED macro manifest: 5,112 rows, 5 macro columns, 2007-01-01 to 2026-05-01.
- `uv run python scripts/run_baseline_backtest.py` completed.
- Baseline report generated at `artifacts/reports/baseline_equal_weight.md`.
- Baseline metrics: annualized return 0.0735, annualized volatility 0.1147, Sharpe ratio 0.6404, max drawdown -0.3240.

## Blocker / Decision Needed

- None.

## Closeout State

- Done.
