# MRPL-009 - Add Transaction Cost And Turnover Diagnostics

- Owner role: Quant Researcher / Research Engineer
- Status: done
- Lifecycle state: Done
- Risk lane: normal
- Canonical artifact: `artifacts/reports/walk_forward_diagnostic.md`

## Scope

Extend the walk-forward diagnostic with simple turnover and transaction-cost assumptions:

- compute monthly turnover from allocation weight changes;
- apply a documented basis-point cost assumption;
- report gross and net diagnostic metrics;
- keep report wording conservative and non-investment-advice oriented.

## Acceptance Criteria

- Tests cover turnover definition and net-return accounting.
- Walk-forward report states the cost assumption.
- Generated return table includes turnover, cost, and net return columns.
- Current strategy claims remain diagnostic only.

## Verification Evidence

- `uv run pytest`: 14 passed.
- `uv run ruff check .`: all checks passed.
- `uv run python scripts/run_walk_forward.py` completed.
- Walk-forward returns table includes turnover, cost, and net return columns.
- Walk-forward diagnostic report states the 5.0 bps one-way turnover cost assumption.
- Average monthly turnover: regime diagnostic 0.1236; equal weight 0.0023.
- Net diagnostic metrics: regime diagnostic annualized return 0.0933, volatility 0.1391, Sharpe 0.6706, max drawdown -0.2807; equal weight annualized return 0.0669, volatility 0.0970, Sharpe 0.6901, max drawdown -0.2789.

## Blocker / Decision Needed

- None.

## Closeout State

- Done.
