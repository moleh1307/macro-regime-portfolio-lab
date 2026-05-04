# MRPL-017 - Design Validation Protocol

- Owner role: Quant Researcher / QA Lead
- Status: ready
- Lifecycle state: Ready
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

- Pending.

## Blocker / Decision Needed

- None.

## Closeout State

- Ready.
