# MRPL-020 - Design Turnover Stability Protocol

- Owner role: Quant Researcher / QA Lead
- Status: ready
- Lifecycle state: Ready
- Risk lane: normal
- Canonical artifact: `docs/turnover-stability-protocol.md`

## Scope

Design the next methodology protocol after MRPL-019 found that the locked
validation result is a partial pass but has unstable validation turnover.

This task should not tune directly to the MRPL-018 validation window. It should
define research-window-only diagnostics and candidate rule families that make
future validation attempts less vulnerable to turnover instability.

## Acceptance Criteria

- Preserve the MRPL-018 result as a partial validation, not a fresh tuning
  target.
- Define research-window turnover-stability diagnostics.
- Define a second-cycle selection objective that penalizes turnover instability.
- Identify simple allocation-rule candidates worth testing.
- Define how any second validation attempt must be labeled, given that the
  2022-forward holdout has already been inspected once.
- Keep all language diagnostic and avoid performance claims.

## Verification Evidence

- Pending.

## Blocker / Decision Needed

- None.

## Closeout State

- Ready.
