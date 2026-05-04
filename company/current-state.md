# Current State

## Capsule

- Objective: Build the reproducible foundation for Macro Regime Portfolio Lab.
- Latest status: MRPL-016 robustness review suite completed, verified, and pushed.
- Operating mode: build.
- Current milestone: Milestone 2 - first point-in-time regime features and walk-forward evaluation protocol.
- Canonical workspace/repo: `/Users/melihkarakose/Projects/Active/macro-regime-portfolio-lab`; `https://github.com/moleh1307/macro-regime-portfolio-lab`
- Current canonical artifact/output: `artifacts/reports/walk_forward_diagnostic.md`; feature outputs remain generated locally under `data/processed/`.
- Current active workflow: `uv sync`, `uv run pytest`, `uv run python scripts/fetch_data.py`, `uv run python scripts/run_baseline_backtest.py`, `uv run python scripts/build_features.py`, `uv run python scripts/run_walk_forward.py`, `uv run python scripts/run_parameter_sensitivity.py`, `uv run python scripts/run_robustness_review.py`.
- Known caveats: no outperformance claims should be made from milestone 2; MRPL-016 found that the default diagnostic beats equal weight full-sample but not static 60/40, rolling-window evidence is uneven, and block-bootstrap Sharpe-difference intervals cross zero.
- Latest diagnostic snapshot: default walk-forward net Sharpe is 0.7392 vs equal-weight 0.6901 and static 60/40 0.8005; rolling 36-month windows beat equal weight in 86/180 windows and static 60/40 in 69/180 windows; buffers 0.10, 0.20, and 0.50 each beat equal weight in 8/19 calendar years.
- Next action: Execute MRPL-017 validation protocol design.
- Blockers: none.

## Capability Surface

- Available: filesystem, shell, local git, Python/uv if installed, network access for public data.
- Required now: MRPL-017 validation protocol design.
- Missing / uncertain: whether a pre-declared validation protocol will preserve any diagnostic edge after parameter selection is constrained.
- Risk boundary: no credentials, paid data, live trading, or release tag without explicit boundary check.
- Approval lane: autonomous for initial public repo creation/push after Melih delegated the choice; confirmation needed for future release tags or changing license.
- Verification path: completed `uv run pytest`, `uv run ruff check .`, public-data manifest inspection, baseline report inspection, feature manifest inspection, walk-forward report inspection, local git commit check, GitHub repo metadata check, remote tracking check, `git ls-remote` check, milestone 2 planning push verification, MRPL-007 push verification, MRPL-008 push verification, MRPL-009 push verification, MRPL-010 push verification, MRPL-011 push verification, MRPL-012 push verification, MRPL-013 push verification, MRPL-014 push verification, MRPL-015 push verification, and MRPL-016 push verification.
