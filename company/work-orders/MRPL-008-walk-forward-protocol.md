# MRPL-008 - Implement Walk-Forward Evaluation Protocol

- Owner role: Quant Researcher / Research Engineer
- Status: ready
- Lifecycle state: Ready
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

- Pending.

## Blocker / Decision Needed

- Depends on MRPL-007.

## Closeout State

- Ready.
