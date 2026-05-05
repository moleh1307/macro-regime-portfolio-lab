# MRPL-023 - Design Fresh-Data-Forward Monitoring Protocol

- Owner role: Quant Researcher / Methodology Reviewer
- Status: done
- Lifecycle state: Completed
- Risk lane: normal
- Canonical artifact: `docs/fresh-data-forward-monitoring-protocol.md`

## Scope

Design a protocol for monitoring newly arriving monthly data after the current
already-inspected sample, using the MRPL-021 turnover-stable branch as the
current research default.

This task should prevent repeated post-holdout redesign from being mistaken for
new validation evidence.

## Acceptance Criteria

- Define the monitoring start boundary relative to the current cached data.
- Freeze the MRPL-021 research-branch default configuration for monitoring.
- Specify which metrics are tracked monthly without changing the rule.
- Define what counts as a monitoring warning versus evidence worth preserving.
- Define report language that distinguishes fresh forward monitoring from
  backfilled/post-holdout diagnostics.
- Write `docs/fresh-data-forward-monitoring-protocol.md`.
- Do not implement data refresh automation yet unless a separate work order is
  created.

## Verification Evidence

- Created `docs/fresh-data-forward-monitoring-protocol.md`.
- Defined source/data boundaries from current local manifests: yfinance through 2026-05-04, FRED through 2026-05-01, monthly features through 2026-04-30, realized turnover-stability return table through the 2026-03-31 signal row.
- Defined 2026-04-30 as the first forward-monitoring signal row, with realized return recorded only after complete May 2026 month-end prices are available.
- Froze the MRPL-021 research branch for monitoring: switch-score buffer 0.50, min regime history 12, top_n 3, max monthly turnover 0.15, 12-month turnover metric warmup, fallback SHY, 5 bps cost.
- Defined monthly metrics, warning rules, evidence handling, allowed language, and implementation artifact paths.
- Updated README with a link to the protocol.

## Blocker / Decision Needed

- None.

## Closeout State

- Completed. Next work should implement the fresh-data-forward monitoring report scaffold without adding data-refresh automation.
