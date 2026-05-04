# Current State

## Capsule

- Objective: Build the reproducible foundation for Macro Regime Portfolio Lab.
- Latest status: Public GitHub repo created and pushed after verified milestone 1 local setup.
- Operating mode: build.
- Current milestone: Milestone 2 - first point-in-time regime features and walk-forward evaluation protocol.
- Canonical workspace/repo: `/Users/melihkarakose/Projects/Active/macro-regime-portfolio-lab`; `https://github.com/moleh1307/macro-regime-portfolio-lab`
- Current canonical artifact/output: `docs/milestone-2-regime-plan.md`; previous baseline report remains `artifacts/reports/baseline_equal_weight.md`.
- Current active workflow: `uv sync`, `uv run pytest`, `uv run python scripts/fetch_data.py`, `uv run python scripts/run_baseline_backtest.py`.
- Known caveats: no outperformance claims should be made from milestone 2 until point-in-time feature alignment and walk-forward evaluation are verified; future release tags still need explicit boundary check.
- Next action: Implement MRPL-007 monthly regime feature pipeline.
- Blockers: none.

## Capability Surface

- Available: filesystem, shell, local git, Python/uv if installed, network access for public data.
- Required now: monthly feature pipeline implementation.
- Missing / uncertain: exact performance implications of the first regime design; must remain unclaimed until tested.
- Risk boundary: no credentials, paid data, live trading, or release tag without explicit boundary check.
- Approval lane: autonomous for initial public repo creation/push after Melih delegated the choice; confirmation needed for future release tags or changing license.
- Verification path: completed `uv run pytest`, `uv run ruff check .`, public-data manifest inspection, baseline report inspection, local git commit check, GitHub repo metadata check, remote tracking check, and `git ls-remote` check.
