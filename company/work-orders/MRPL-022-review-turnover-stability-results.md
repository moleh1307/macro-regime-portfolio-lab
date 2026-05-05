# MRPL-022 - Review Turnover Stability Results

- Owner role: Quant Researcher / Methodology Reviewer
- Status: done
- Lifecycle state: Completed
- Risk lane: normal
- Canonical artifact: `docs/turnover-stability-review.md`

## Scope

Review the MRPL-021 turnover-stability result and decide how to interpret the
second-cycle diagnostic branch.

This task must preserve the MRPL-018 locked validation result and the MRPL-021
post-holdout-review label. It should not convert the second-cycle diagnostic
into an outperformance claim.

## Acceptance Criteria

- Summarize what MRPL-021 improved and what it did not improve.
- Compare turnover-stability result behavior against MRPL-018 validation and
  benchmark hurdles.
- Decide whether the second-cycle protocol should be treated as current
  research-branch default, diagnostic branch only, or an input to a future
  fresh-data-forward monitoring protocol.
- Identify any next methodology work without tuning directly to 2022-forward
  outcomes.
- Write `docs/turnover-stability-review.md`.
- Update README or project state only if the review changes the public-facing
  interpretation boundary.

## Verification Evidence

- Created `docs/turnover-stability-review.md`.
- Reviewed MRPL-021 as a post-holdout-review diagnostic, not fresh validation.
- Compared MRPL-021 turnover against MRPL-018: average monthly turnover fell from 0.2304 to 0.0435 in the 2022-forward diagnostic slice.
- Preserved the weaker performance result: MRPL-021 regime diagnostic net Sharpe 0.8194 trails equal weight 0.8266 and SHY 1.1053.
- Decided MRPL-021 should be treated as the current research-branch default for future methodology work, not as a validated strategy.
- Identified fresh-data-forward monitoring protocol as the next methodology task.
- Updated README with a link to the review.

## Blocker / Decision Needed

- None.

## Closeout State

- Completed. Next work should design a fresh-data-forward monitoring protocol.
