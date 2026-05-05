# Current State

## Capsule

- Objective: Build the reproducible foundation for Macro Regime Portfolio Lab.
- Latest status: MRPL-025 milestone 2 boundary reviewed; milestone 2 is coherent as a public research-process artifact.
- Operating mode: build.
- Current milestone: Milestone 2 - first point-in-time regime features and walk-forward evaluation protocol.
- Canonical workspace/repo: `/Users/melihkarakose/Projects/Active/macro-regime-portfolio-lab`; `https://github.com/moleh1307/macro-regime-portfolio-lab`
- Current canonical artifact/output: `docs/milestone-2-research-summary.md`; fresh-forward tables live under `artifacts/reports/fresh_forward_monitoring_*`.
- Current active workflow: `uv sync`, `uv run pytest`, `uv run python scripts/fetch_data.py`, `uv run python scripts/run_baseline_backtest.py`, `uv run python scripts/build_features.py`, `uv run python scripts/run_walk_forward.py`, `uv run python scripts/run_parameter_sensitivity.py`, `uv run python scripts/run_robustness_review.py`, `uv run python scripts/run_validation_protocol.py`, `uv run python scripts/run_turnover_stability_protocol.py`, `uv run python scripts/run_fresh_forward_monitoring.py`.
- Known caveats: no outperformance claims should be made from milestone 2; MRPL-018 remains the first locked validation result; MRPL-021 is a post-holdout-review diagnostic because the 2022-forward period had already been inspected.
- Latest methodology protocol/result: MRPL-025 summarizes milestone 2 as a serious reproducible research process, not a performance proof. Next work should improve README/docs scanability without changing methodology.
- Next action: Execute MRPL-026 public README and docs navigation polish.
- Blockers: none.

## Capability Surface

- Available: filesystem, shell, local git, Python/uv if installed, network access for public data.
- Required now: MRPL-026 public README and docs navigation polish.
- Missing / uncertain: best compact README layout for GitHub readers.
- Risk boundary: no credentials, paid data, live trading, or release tag without explicit boundary check.
- Approval lane: autonomous for initial public repo creation/push after Melih delegated the choice; confirmation needed for future release tags or changing license.
- Verification path: completed `uv run pytest`, `uv run ruff check .`, public-data manifest inspection, baseline report inspection, feature manifest inspection, walk-forward report inspection, local git commit check, GitHub repo metadata check, remote tracking check, `git ls-remote` check, milestone 2 planning push verification, MRPL-007 push verification, MRPL-008 push verification, MRPL-009 push verification, MRPL-010 push verification, MRPL-011 push verification, MRPL-012 push verification, MRPL-013 push verification, MRPL-014 push verification, MRPL-015 push verification, MRPL-016 push verification, MRPL-017 push verification, MRPL-018 push verification, MRPL-019 push verification, MRPL-020 push verification, MRPL-021 push verification, MRPL-022 push verification, MRPL-023 push verification, MRPL-024 push verification, and MRPL-025 document review.
