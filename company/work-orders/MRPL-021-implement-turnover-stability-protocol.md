# MRPL-021 - Implement Turnover Stability Protocol

- Owner role: Data Engineer / Quant Researcher
- Status: ready
- Lifecycle state: Ready
- Risk lane: normal
- Canonical artifact: `docs/turnover-stability-results.md`

## Scope

Implement the MRPL-020 turnover stability protocol.

This is a post-holdout-review diagnostic task. The 2022-forward period has
already been inspected in MRPL-018, so results must not be described as fresh
independent validation.

## Acceptance Criteria

- Add turnover-stability metrics in a reusable module.
- Add second-cycle candidate configuration.
- Select candidates using only the research/calibration window.
- Reject candidates that fail hard turnover-stability thresholds before ranking.
- Generate post-holdout-review artifacts under
  `artifacts/reports/turnover_stability_*`.
- Write `docs/turnover-stability-results.md`.
- Add tests proving research-window-only selection and required
  post-holdout-review labeling.
- Keep all report language diagnostic and avoid outperformance claims.

## Verification Evidence

- Pending.

## Blocker / Decision Needed

- None.

## Closeout State

- Ready.
