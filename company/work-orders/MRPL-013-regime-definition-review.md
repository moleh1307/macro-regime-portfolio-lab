# MRPL-013 - Review Regime Definition

- Owner role: Quant Researcher / Replication QA
- Status: done
- Lifecycle state: Done
- Risk lane: normal
- Canonical artifact: `docs/regime-definition-review.md`

## Scope

Review whether the current four-state regime definition is too weak or too noisy:

- inspect regime counts and persistence;
- inspect feature thresholds and whether binary growth/inflation axes are too crude;
- compare current labels against major historical periods qualitatively;
- propose one conservative refinement or explicitly keep the current labels with rationale.

## Acceptance Criteria

- Create `docs/regime-definition-review.md`.
- Identify whether the current regime definition should remain the milestone default.
- Do not introduce a complex ML regime model yet.
- Keep conclusions diagnostic and non-investment-advice oriented.

## Verification Evidence

- Created `docs/regime-definition-review.md`.
- Inspected current regime counts, persistence, feature thresholds, and selected historical periods.
- Found that the current OR-based growth rule labels 200 of 216 months as improving growth.
- Reviewed a stricter both-confirmation growth rule requiring unemployment improvement and positive SPY trend.
- Alternative both-confirmation rule changes 70 labels and produces a more balanced distribution: improving/easing 59, improving/rising 71, weakening/easing 51, weakening/rising 35.
- Recommended implementing the stricter growth definition next while keeping inflation labeling unchanged for now.

## Blocker / Decision Needed

- None.

## Closeout State

- Done.
