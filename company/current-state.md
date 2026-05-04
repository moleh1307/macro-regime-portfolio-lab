# Current State

## Capsule

- Objective: Build the reproducible foundation for Macro Regime Portfolio Lab.
- Latest status: MRPL-007 monthly regime feature pipeline implemented, verified, and ready to push.
- Operating mode: build.
- Current milestone: Milestone 2 - first point-in-time regime features and walk-forward evaluation protocol.
- Canonical workspace/repo: `/Users/melihkarakose/Projects/Active/macro-regime-portfolio-lab`; `https://github.com/moleh1307/macro-regime-portfolio-lab`
- Current canonical artifact/output: `data/processed/monthly_features.csv` and `data/processed/monthly_features_manifest.json` generated locally; `docs/milestone-2-regime-plan.md` remains the milestone plan.
- Current active workflow: `uv sync`, `uv run pytest`, `uv run python scripts/fetch_data.py`, `uv run python scripts/run_baseline_backtest.py`, `uv run python scripts/build_features.py`.
- Known caveats: no outperformance claims should be made from milestone 2 until point-in-time feature alignment and walk-forward evaluation are verified; future release tags still need explicit boundary check.
- Next action: Implement MRPL-008 walk-forward evaluation protocol.
- Blockers: none.

## Capability Surface

- Available: filesystem, shell, local git, Python/uv if installed, network access for public data.
- Required now: walk-forward protocol implementation.
- Missing / uncertain: exact performance implications of the first regime design; must remain unclaimed until walk-forward evaluation is implemented and tested.
- Risk boundary: no credentials, paid data, live trading, or release tag without explicit boundary check.
- Approval lane: autonomous for initial public repo creation/push after Melih delegated the choice; confirmation needed for future release tags or changing license.
- Verification path: completed `uv run pytest`, `uv run ruff check .`, public-data manifest inspection, baseline report inspection, feature manifest inspection, local git commit check, GitHub repo metadata check, remote tracking check, `git ls-remote` check, and milestone 2 planning push verification.
