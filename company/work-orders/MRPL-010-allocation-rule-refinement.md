# MRPL-010 - Refine Diagnostic Allocation Rule

- Owner role: Quant Researcher / Replication QA
- Status: ready
- Lifecycle state: Ready
- Risk lane: normal
- Canonical artifact: `docs/allocation-rule-review.md`

## Scope

Review and refine the current diagnostic allocation rule before making further performance comparisons:

- inspect concentration and regime-specific asset choices;
- decide whether top-`n` same-regime average return is too naive;
- consider capped weights, defensive sleeves, or volatility-aware ranking;
- keep the result as a diagnostic research rule, not a deployable strategy.

## Acceptance Criteria

- Create a short allocation-rule review document.
- Identify one conservative refinement or explicitly keep the current rule with rationale.
- Add tests if the allocation rule changes.
- Report wording continues to avoid robustness or investment claims.

## Verification Evidence

- Pending.

## Blocker / Decision Needed

- None.

## Closeout State

- Ready.
