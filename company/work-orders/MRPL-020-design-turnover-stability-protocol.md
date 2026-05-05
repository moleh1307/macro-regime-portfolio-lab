# MRPL-020 - Design Turnover Stability Protocol

- Owner role: Quant Researcher / QA Lead
- Status: done
- Lifecycle state: Completed
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

- Created `docs/turnover-stability-protocol.md`.
- Preserved MRPL-018 as the first locked validation result and partial validation.
- Defined that future 2022-forward runs must be labeled `post-holdout-review diagnostic`.
- Defined research-window-only turnover stability diagnostics and initial thresholds.
- Defined a second-cycle selection objective that penalizes turnover instability and allocation complexity.
- Identified simple candidate rule families: top-2, top-3, stricter replacement margin, max monthly turnover guard, and defensive sleeve cap.
- Kept benchmark panel unchanged: equal weight, static SPY/TLT 60/40, SHY.
- Added README pointer to the turnover stability protocol.
- Created MRPL-021 implementation work order.

## Blocker / Decision Needed

- None.

## Closeout State

- Completed. Next work is implementation of the turnover stability protocol.
