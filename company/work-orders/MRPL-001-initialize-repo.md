# MRPL-001 - Initialize Standalone Repo And Reproducibility Scaffold

- Owner role: Founder / Research Engineer
- Status: done
- Lifecycle state: Done
- Risk lane: normal
- Canonical artifact: `/Users/melihkarakose/Projects/Active/macro-regime-portfolio-lab`

## Scope

Create the initial local repo structure for a standalone GitHub-bound quant research project:

- README with scope, stack, and milestone 1.
- Python package scaffold.
- Public-data source configuration.
- Conservative v0 ETF universe.
- CLI scripts for data fetch and baseline backtest.
- Simple custom monthly equal-weight backtester.
- Local tests for config and backtest logic.
- Minimal JARVIS Specialist project state.

## Acceptance Criteria

- Project exists in the canonical active projects directory.
- Scope reflects Melih's setup decisions.
- No live-trading or brokerage integration is included.
- Data cache directories are ignored by git by default.
- Tests can be run locally with `uv run pytest`.
- Task board and current state agree on the next task.

## Verification Evidence

- `uv sync` completed and installed the local package.
- `uv run pytest`: 4 passed.
- `uv run ruff check .`: all checks passed.

## Blocker / Decision Needed

- None for local scaffold.
- License remains TBD before public release.

## Closeout State

- Done.
