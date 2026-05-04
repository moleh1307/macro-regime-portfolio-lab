# Current State

## Capsule

- Objective: Build the reproducible foundation for Macro Regime Portfolio Lab.
- Latest status: Public GitHub repo created and pushed after verified milestone 1 local setup.
- Operating mode: build.
- Current milestone: Milestone 1 - public-data cache, custom baseline backtester, one baseline report.
- Canonical workspace/repo: `/Users/melihkarakose/Projects/Active/macro-regime-portfolio-lab`; `https://github.com/moleh1307/macro-regime-portfolio-lab`
- Current canonical artifact/output: `artifacts/reports/baseline_equal_weight.md`; data manifests are in ignored raw-data cache folders.
- Current active workflow: `uv sync`, `uv run pytest`, `uv run python scripts/fetch_data.py`, `uv run python scripts/run_baseline_backtest.py`.
- Known caveats: no outperformance claims should be made in milestone 1; future release tags still need explicit boundary check.
- Next action: Start milestone 2 planning only after reviewing methodology risks and deciding the first regime-feature design.
- Blockers: none.

## Capability Surface

- Available: filesystem, shell, local git, Python/uv if installed, network access for public data.
- Required now: next milestone planning.
- Missing / uncertain: exact milestone 2 regime definition and evaluation protocol.
- Risk boundary: no credentials, paid data, live trading, or release tag without explicit boundary check.
- Approval lane: autonomous for initial public repo creation/push after Melih delegated the choice; confirmation needed for future release tags or changing license.
- Verification path: completed `uv run pytest`, `uv run ruff check .`, public-data manifest inspection, baseline report inspection, local git commit check, GitHub repo metadata check, remote tracking check, and `git ls-remote` check.
