# MRPL-011 - Add Turnover Control And Cost Sensitivity Review

- Owner role: Quant Researcher / Replication QA
- Status: done
- Lifecycle state: Done
- Risk lane: normal
- Canonical artifact: `docs/turnover-cost-sensitivity.md`

## Scope

Review whether the diagnostic allocation rule is overly sensitive to turnover and cost assumptions:

- summarize turnover after the risk-adjusted allocation refinement;
- test whether simple turnover controls are needed before further strategy work;
- consider no-trade bands, minimum holding periods, or top-asset stability rules;
- document cost sensitivity without claiming robustness.

## Acceptance Criteria

- Create a turnover/cost sensitivity note.
- Identify whether a turnover control should be implemented next.
- If code changes are made, tests cover the turnover-control behavior.
- Public report wording remains diagnostic only.

## Verification Evidence

- Created `docs/turnover-cost-sensitivity.md`.
- Implemented a simple switch-score buffer: keep previous basket unless candidate basket score exceeds previous basket score by the configured buffer.
- Default buffer: 0.10.
- Added tests for keeping prior assets without enough score improvement and accepting large score improvement.
- `uv run pytest`: 17 passed.
- `uv run ruff check .`: all checks passed.
- `uv run python scripts/run_walk_forward.py` completed.
- Observed result: average monthly turnover fell from 0.1733 to 0.0314, but regime diagnostic net Sharpe fell from 0.6534 to 0.5903; equal-weight net Sharpe remained 0.6901.

## Blocker / Decision Needed

- None.

## Closeout State

- Done.
