# MRPL-024 - Implement Fresh-Data-Forward Monitoring Report Scaffold

- Owner role: Data Engineer / Quant Researcher
- Status: ready
- Lifecycle state: Ready
- Risk lane: normal
- Canonical artifact: `docs/fresh-data-forward-monitoring.md`

## Scope

Implement the report scaffold from `docs/fresh-data-forward-monitoring-protocol.md`.

This task should create the monitoring machinery and produce a report that is
honest about the current boundary. It should not add data-refresh automation or
pretend partial May 2026 data creates a completed forward-monitoring return.

## Acceptance Criteria

- Add a reproducible CLI script for the frozen MRPL-021 monitoring branch.
- Use current cached data only.
- Generate separate monitoring artifacts under
  `artifacts/reports/fresh_forward_monitoring_*`.
- Write `docs/fresh-data-forward-monitoring.md`.
- If no completed forward-monitoring return exists yet, the report must say so
  explicitly and still record the first pending signal row.
- Add tests for boundary handling and no-backfill behavior.
- Keep language diagnostic and avoid validation/outperformance claims.

## Verification Evidence

- Pending.

## Blocker / Decision Needed

- None.

## Closeout State

- Ready.
