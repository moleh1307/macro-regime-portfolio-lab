# MRPL-018 - Implement Validation Protocol

- Owner role: Data Engineer / Quant Researcher
- Status: ready
- Lifecycle state: Ready
- Risk lane: normal
- Canonical artifact: `docs/validation-results.md`

## Scope

Implement the MRPL-017 validation protocol in code and generate the first
validation result artifacts.

The implementation must preserve the locked validation boundary and avoid using
2022-forward data for parameter selection.

## Acceptance Criteria

- Add validation configuration for the fixed split and candidate grid.
- Add `scripts/run_validation_protocol.py` or equivalent reproducible CLI entry
  point.
- Select configurable parameters using only the research/calibration window.
- Evaluate the selected configuration once on the locked validation window.
- Compare against equal weight, static SPY/TLT 60/40, and SHY defensive proxy.
- Write machine-readable artifacts under `artifacts/reports/validation_*`.
- Write `docs/validation-results.md` with pass/fail language from
  `docs/validation-protocol.md`.
- Add tests for split boundaries and to verify selection excludes validation rows.

## Verification Evidence

- Pending.

## Blocker / Decision Needed

- None.

## Closeout State

- Ready.
