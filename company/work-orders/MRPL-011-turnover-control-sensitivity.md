# MRPL-011 - Add Turnover Control And Cost Sensitivity Review

- Owner role: Quant Researcher / Replication QA
- Status: ready
- Lifecycle state: Ready
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

- Pending.

## Blocker / Decision Needed

- None.

## Closeout State

- Ready.
