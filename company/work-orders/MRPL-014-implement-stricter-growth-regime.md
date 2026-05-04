# MRPL-014 - Implement Stricter Growth Regime Definition

- Owner role: Data Engineer / Quant Researcher
- Status: ready
- Lifecycle state: Ready
- Risk lane: normal
- Canonical artifact: `data/processed/monthly_features.csv`

## Scope

Implement the MRPL-013 recommendation:

- change growth classification from OR confirmation to both-confirmation;
- keep inflation classification unchanged;
- regenerate monthly features and manifests;
- regenerate walk-forward and parameter sensitivity artifacts;
- update docs/report wording if needed.

## Acceptance Criteria

- Tests cover the stricter growth classification behavior.
- Feature table regime counts reflect the stricter rule.
- Walk-forward and sensitivity artifacts are regenerated.
- Current report wording remains diagnostic only.

## Verification Evidence

- Pending.

## Blocker / Decision Needed

- None.

## Closeout State

- Ready.
