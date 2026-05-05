# Current State

## Capsule

- Objective: Build the reproducible foundation for Macro Regime Portfolio Lab.
- Latest status: MRPL-021 turnover stability protocol implemented, verified locally, and ready to push.
- Operating mode: build.
- Current milestone: Milestone 2 - first point-in-time regime features and walk-forward evaluation protocol.
- Canonical workspace/repo: `/Users/melihkarakose/Projects/Active/macro-regime-portfolio-lab`; `https://github.com/moleh1307/macro-regime-portfolio-lab`
- Current canonical artifact/output: `docs/turnover-stability-results.md`; post-holdout-review tables live under `artifacts/reports/turnover_stability_*`.
- Current active workflow: `uv sync`, `uv run pytest`, `uv run python scripts/fetch_data.py`, `uv run python scripts/run_baseline_backtest.py`, `uv run python scripts/build_features.py`, `uv run python scripts/run_walk_forward.py`, `uv run python scripts/run_parameter_sensitivity.py`, `uv run python scripts/run_robustness_review.py`, `uv run python scripts/run_validation_protocol.py`, `uv run python scripts/run_turnover_stability_protocol.py`.
- Known caveats: no outperformance claims should be made from milestone 2; MRPL-018 remains the first locked validation result; MRPL-021 is a post-holdout-review diagnostic because the 2022-forward period had already been inspected.
- Latest methodology protocol/result: turnover stability is implemented as a second-cycle diagnostic gate. Candidate rules must pass research-window turnover thresholds before ranking. MRPL-021 selected buffer 0.50, min regime history 12, top_n 3, max monthly turnover 0.15, and 12-month turnover metric warmup.
- Next action: Execute MRPL-022 turnover stability result review.
- Blockers: none.

## Capability Surface

- Available: filesystem, shell, local git, Python/uv if installed, network access for public data.
- Required now: MRPL-022 turnover stability result review.
- Missing / uncertain: whether the second-cycle protocol should become the current research branch default, remain a diagnostic branch, or be followed by a fresh-data-forward monitoring protocol.
- Risk boundary: no credentials, paid data, live trading, or release tag without explicit boundary check.
- Approval lane: autonomous for initial public repo creation/push after Melih delegated the choice; confirmation needed for future release tags or changing license.
- Verification path: completed `uv run pytest`, `uv run ruff check .`, public-data manifest inspection, baseline report inspection, feature manifest inspection, walk-forward report inspection, local git commit check, GitHub repo metadata check, remote tracking check, `git ls-remote` check, milestone 2 planning push verification, MRPL-007 push verification, MRPL-008 push verification, MRPL-009 push verification, MRPL-010 push verification, MRPL-011 push verification, MRPL-012 push verification, MRPL-013 push verification, MRPL-014 push verification, MRPL-015 push verification, MRPL-016 push verification, MRPL-017 push verification, MRPL-018 push verification, MRPL-019 push verification, MRPL-020 push verification, and MRPL-021 local verification.
