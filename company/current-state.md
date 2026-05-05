# Current State

## Capsule

- Objective: Build the reproducible foundation for Macro Regime Portfolio Lab.
- Latest status: MRPL-020 turnover stability protocol designed, verified, and pushed.
- Operating mode: build.
- Current milestone: Milestone 2 - first point-in-time regime features and walk-forward evaluation protocol.
- Canonical workspace/repo: `/Users/melihkarakose/Projects/Active/macro-regime-portfolio-lab`; `https://github.com/moleh1307/macro-regime-portfolio-lab`
- Current canonical artifact/output: `artifacts/reports/walk_forward_diagnostic.md`; feature outputs remain generated locally under `data/processed/`.
- Current active workflow: `uv sync`, `uv run pytest`, `uv run python scripts/fetch_data.py`, `uv run python scripts/run_baseline_backtest.py`, `uv run python scripts/build_features.py`, `uv run python scripts/run_walk_forward.py`, `uv run python scripts/run_parameter_sensitivity.py`, `uv run python scripts/run_robustness_review.py`, `uv run python scripts/run_validation_protocol.py`.
- Known caveats: no outperformance claims should be made from milestone 2; MRPL-020 preserves MRPL-018 as the first locked validation result and requires future 2022-forward runs to be labeled post-holdout-review diagnostics.
- Latest methodology protocol: turnover stability is the next gate; candidate rules must pass research-window turnover thresholds before ranking, and second-cycle selection penalizes turnover instability and allocation complexity.
- Next action: Execute MRPL-021 turnover stability protocol implementation.
- Blockers: none.

## Capability Surface

- Available: filesystem, shell, local git, Python/uv if installed, network access for public data.
- Required now: MRPL-021 turnover stability protocol implementation.
- Missing / uncertain: whether research-window turnover-stability filters will reduce post-holdout-review turnover instability without erasing the useful equal-weight validation edge.
- Risk boundary: no credentials, paid data, live trading, or release tag without explicit boundary check.
- Approval lane: autonomous for initial public repo creation/push after Melih delegated the choice; confirmation needed for future release tags or changing license.
- Verification path: completed `uv run pytest`, `uv run ruff check .`, public-data manifest inspection, baseline report inspection, feature manifest inspection, walk-forward report inspection, local git commit check, GitHub repo metadata check, remote tracking check, `git ls-remote` check, milestone 2 planning push verification, MRPL-007 push verification, MRPL-008 push verification, MRPL-009 push verification, MRPL-010 push verification, MRPL-011 push verification, MRPL-012 push verification, MRPL-013 push verification, MRPL-014 push verification, MRPL-015 push verification, MRPL-016 push verification, MRPL-017 push verification, MRPL-018 push verification, MRPL-019 push verification, and MRPL-020 push verification.
