# MRPL-021 - Implement Turnover Stability Protocol

- Owner role: Data Engineer / Quant Researcher
- Status: done
- Lifecycle state: Completed
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

- Added `configs/turnover_stability.yml`.
- Added `src/macro_regime_portfolio_lab/turnover_stability.py`.
- Added `scripts/run_turnover_stability_protocol.py`.
- Added tests for turnover-stability metrics, research-window-only selection, rejected-candidate handling, config parsing, and post-holdout-review labeling.
- Generated `docs/turnover-stability-results.md`.
- Generated post-holdout-review tables under `artifacts/reports/turnover_stability_*`.
- Selected second-cycle diagnostic configuration: switch-score buffer 0.50, min regime history 12, top_n 3, max monthly turnover 0.15, turnover metric warmup 12 months, fallback SHY, 5 bps one-way cost.
- Candidate screen: 24 candidates passed hard turnover-stability thresholds; 48 were rejected before ranking.
- Post-holdout-review interpretation: turnover stability reduced the known turnover failure mode, but this is not fresh independent validation.
- `uv run pytest` passed with 33 tests.
- `uv run ruff check .` passed.
- `uv run python scripts/run_turnover_stability_protocol.py` completed and regenerated the report/artifacts.

## Blocker / Decision Needed

- None.

## Closeout State

- Completed. Next work should review the turnover-stability result and decide whether the second-cycle protocol is worth preserving as a research branch, without strengthening public performance claims.
