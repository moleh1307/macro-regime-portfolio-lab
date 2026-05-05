# MRPL-023 - Design Fresh-Data-Forward Monitoring Protocol

- Owner role: Quant Researcher / Methodology Reviewer
- Status: ready
- Lifecycle state: Ready
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

- Pending.

## Blocker / Decision Needed

- None.

## Closeout State

- Ready.
