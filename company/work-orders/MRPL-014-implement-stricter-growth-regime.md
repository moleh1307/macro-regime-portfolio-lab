# MRPL-014 - Implement Stricter Growth Regime Definition

- Owner role: Data Engineer / Quant Researcher
- Status: done
- Lifecycle state: Completed
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

- Implemented growth classification as both-confirmation: `unemployment_3m_change <= 0` and `spy_10m_trend == 1` are both required for `improving_growth`; all other combinations become `weakening_growth`.
- Added unit coverage for the stricter growth classification behavior.
- Regenerated `data/processed/monthly_features.csv` and manifest locally.
- Regenerated `artifacts/reports/walk_forward_diagnostic.md`, `artifacts/reports/walk_forward_returns.csv`, `artifacts/reports/walk_forward_weights.csv`, and `artifacts/reports/parameter_sensitivity.csv`.
- Feature table verification: 216 rows, 2008-05-31 to 2026-04-30; growth counts are 130 improving and 86 weakening.
- Full regime counts: improving/easing 59, improving/rising 71, weakening/easing 51, weakening/rising 35.
- Default walk-forward diagnostic: regime net Sharpe 0.7392 vs equal-weight net Sharpe 0.6901 at 5 bps cost and 0.10 switch-score buffer.
- Sensitivity grid top diagnostic setting: switch-score buffer 0.50, 0 bps cost, strategy net Sharpe 0.9821 vs equal-weight net Sharpe 0.6903.
- `uv run pytest` passed: 19 tests.
- `uv run ruff check .` passed.

## Blocker / Decision Needed

- None.

## Closeout State

- Completed. Next work should review the post-change diagnostics before promoting any public claim.
