# MRPL-008 - Implement Walk-Forward Evaluation Protocol

- Owner role: Quant Researcher / Research Engineer
- Status: done
- Lifecycle state: Done
- Risk lane: normal
- Canonical artifact: `docs/walk-forward-evaluation.md`

## Scope

After MRPL-007, implement the evaluation protocol needed before any allocation claims:

- align monthly feature matrix with next-month ETF returns;
- define expanding-window or rolling-window evaluation;
- compare against equal-weight baseline;
- report metrics, regime counts, and caveats.

## Acceptance Criteria

- Walk-forward protocol document exists.
- Code prevents same-month feature/return leakage.
- Report wording avoids robustness or outperformance claims until evidence supports them.

## Verification Evidence

- Created `docs/walk-forward-evaluation.md`.
- Added `src/macro_regime_portfolio_lab/evaluation.py`.
- Added `scripts/run_walk_forward.py`.
- Added tests covering next-month return alignment, shared-date alignment, strict training-history exclusion, and partial target-month exclusion.
- `uv run pytest`: 12 passed.
- `uv run ruff check .`: all checks passed.
- `uv run python scripts/run_walk_forward.py` completed.
- Generated `artifacts/reports/walk_forward_diagnostic.md`.
- Generated `artifacts/reports/walk_forward_returns.csv` with 215 rows from 2008-05-31 to 2026-03-31.
- Generated `artifacts/reports/walk_forward_weights.csv` with 215 rows and 12 ETF weight columns.
- Diagnostic metrics: regime diagnostic annualized return 0.0941, volatility 0.1391, Sharpe 0.6764, max drawdown -0.2804; equal weight annualized return 0.0669, volatility 0.0970, Sharpe 0.6903, max drawdown -0.2789.

## Blocker / Decision Needed

- None.

## Closeout State

- Done.
