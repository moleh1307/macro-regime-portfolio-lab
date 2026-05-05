# Current State

## Capsule

- Objective: Build the reproducible foundation for Macro Regime Portfolio Lab.
- Latest status: MRPL-022 turnover stability results reviewed; MRPL-021 branch adopted as current research-branch default for future methodology work, not as a validated strategy.
- Operating mode: build.
- Current milestone: Milestone 2 - first point-in-time regime features and walk-forward evaluation protocol.
- Canonical workspace/repo: `/Users/melihkarakose/Projects/Active/macro-regime-portfolio-lab`; `https://github.com/moleh1307/macro-regime-portfolio-lab`
- Current canonical artifact/output: `docs/turnover-stability-review.md`; MRPL-021 post-holdout-review tables live under `artifacts/reports/turnover_stability_*`.
- Current active workflow: `uv sync`, `uv run pytest`, `uv run python scripts/fetch_data.py`, `uv run python scripts/run_baseline_backtest.py`, `uv run python scripts/build_features.py`, `uv run python scripts/run_walk_forward.py`, `uv run python scripts/run_parameter_sensitivity.py`, `uv run python scripts/run_robustness_review.py`, `uv run python scripts/run_validation_protocol.py`, `uv run python scripts/run_turnover_stability_protocol.py`.
- Known caveats: no outperformance claims should be made from milestone 2; MRPL-018 remains the first locked validation result; MRPL-021 is a post-holdout-review diagnostic because the 2022-forward period had already been inspected.
- Latest methodology protocol/result: MRPL-022 decided the MRPL-021 turnover-stable branch is the current research-branch default for future methodology work, but not a validated strategy. It improves turnover behavior while trailing equal weight and SHY on 2022-forward net Sharpe.
- Next action: Execute MRPL-023 fresh-data-forward monitoring protocol design.
- Blockers: none.

## Capability Surface

- Available: filesystem, shell, local git, Python/uv if installed, network access for public data.
- Required now: MRPL-023 fresh-data-forward monitoring protocol design.
- Missing / uncertain: exact monitoring start boundary should be defined from the current cached sample and source manifests.
- Risk boundary: no credentials, paid data, live trading, or release tag without explicit boundary check.
- Approval lane: autonomous for initial public repo creation/push after Melih delegated the choice; confirmation needed for future release tags or changing license.
- Verification path: completed `uv run pytest`, `uv run ruff check .`, public-data manifest inspection, baseline report inspection, feature manifest inspection, walk-forward report inspection, local git commit check, GitHub repo metadata check, remote tracking check, `git ls-remote` check, milestone 2 planning push verification, MRPL-007 push verification, MRPL-008 push verification, MRPL-009 push verification, MRPL-010 push verification, MRPL-011 push verification, MRPL-012 push verification, MRPL-013 push verification, MRPL-014 push verification, MRPL-015 push verification, MRPL-016 push verification, MRPL-017 push verification, MRPL-018 push verification, MRPL-019 push verification, MRPL-020 push verification, MRPL-021 push verification, and MRPL-022 document review.
