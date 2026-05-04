# MRPL-017 - Design Validation Protocol

- Owner role: Quant Researcher / QA Lead
- Status: done
- Lifecycle state: Completed
- Risk lane: normal
- Canonical artifact: `docs/validation-protocol.md`

## Scope

Design the next evaluation protocol after MRPL-016 showed that the current
full-sample diagnostic is promising but not claim-grade.

The goal is to prevent choosing regime rules, switch buffers, or benchmarks from
the same full-sample diagnostics used for public claims.

## Acceptance Criteria

- Define a validation split or walk-forward model-selection protocol appropriate
  for the current 2008-2026 monthly sample.
- Specify which parameters are fixed before validation and which can be selected
  only inside training windows.
- Define the benchmark panel to use going forward.
- Define report language allowed after validation, including failure cases.
- Keep the protocol simple enough to implement in the current Python stack.

## Verification Evidence

- Created `docs/validation-protocol.md`.
- Defined locked validation split: research/calibration window from 2008-05-31 through 2021-12-31; locked validation window from 2022-01-31 through 2026-03-31 with current data.
- Defined nested research-window selection rule for `switch_score_buffer`, `min_regime_history`, and `top_n`.
- Fixed first validation benchmark panel: equal-weight ETF universe, static SPY/TLT 60/40, and SHY defensive proxy.
- Defined parameters fixed before validation versus parameters selectable only inside training windows.
- Defined allowed and disallowed report language for pass, partial pass, and failure cases.
- Added README pointer to the validation protocol.
- Created MRPL-018 implementation work order.

## Blocker / Decision Needed

- None.

## Closeout State

- Completed. Next work is implementation of the validation protocol.
