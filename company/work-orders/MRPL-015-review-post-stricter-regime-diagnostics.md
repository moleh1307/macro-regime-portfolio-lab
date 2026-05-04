# MRPL-015 - Review Post-Stricter-Regime Diagnostics

- Owner role: Quant Researcher / QA Lead
- Status: done
- Lifecycle state: Completed
- Risk lane: normal
- Canonical artifact: `docs/post-stricter-regime-diagnostic-review.md`

## Scope

Review the diagnostics generated after MRPL-014 made the stricter growth definition the milestone default.

Focus on whether the improved walk-forward and sensitivity results are methodologically credible enough for limited GitHub portfolio language, not on proving outperformance.

## Acceptance Criteria

- Compare default and sensitivity-grid results against the equal-weight benchmark.
- Identify the main robustness risks behind the stronger post-change metrics.
- Check whether any result is overly dependent on the switch-score buffer or turnover assumptions.
- Recommend the next methodology task before public-facing performance language is strengthened.
- Keep all wording diagnostic and research-scaffold oriented.

## Verification Evidence

- Created `docs/post-stricter-regime-diagnostic-review.md`.
- Compared default walk-forward diagnostics against equal weight: regime net Sharpe 0.7392 vs equal-weight net Sharpe 0.6901 at 5 bps cost and 0.10 switch-score buffer.
- Reviewed parameter sensitivity grid: 12 of 20 rows beat equal weight on net Sharpe; top row is 0.50 switch buffer / 0 bps cost with strategy net Sharpe 0.9821 vs equal-weight 0.6903.
- Identified parameter-dependence risk because the strongest rows use higher switch buffers than the current default.
- Checked calendar-year behavior: default strategy beats equal-weight net return in 8 of 19 calendar years; largest relative gain is 2022, largest relative miss is 2025.
- Checked regime-level monthly mean returns across the four post-MRPL-014 states.
- Updated `docs/parameter-sensitivity.md` so it no longer describes the stale pre-MRPL-014 grid result.
- Created MRPL-016 robustness review suite as the next methodology task.

## Blocker / Decision Needed

- None.

## Closeout State

- Completed. Stronger diagnostics are promising but remain diagnostic only; next work is MRPL-016.
