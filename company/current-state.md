# Current State

## Capsule

- Objective: Build the reproducible foundation for Macro Regime Portfolio Lab.
- Latest status: Initial standalone repo scaffold, public-data cache, baseline backtest, methodology risk review, and local git baseline completed. MIT license selected for public GitHub launch.
- Operating mode: build.
- Current milestone: Milestone 1 - public-data cache, custom baseline backtester, one baseline report.
- Canonical workspace/repo: `/Users/melihkarakose/Projects/Active/macro-regime-portfolio-lab`
- Current canonical artifact/output: `artifacts/reports/baseline_equal_weight.md`; data manifests are in ignored raw-data cache folders.
- Current active workflow: `uv sync`, `uv run pytest`, `uv run python scripts/fetch_data.py`, `uv run python scripts/run_baseline_backtest.py`.
- Known caveats: GitHub remote not created yet; no outperformance claims should be made in milestone 1.
- Next action: Create/push the public GitHub repo and verify remote state.
- Blockers: none for public GitHub creation after Melih delegated the launch choice.

## Capability Surface

- Available: filesystem, shell, local git, Python/uv if installed, network access for public data.
- Required now: GitHub repo creation/push verification.
- Missing / uncertain: GitHub remote creation status.
- Risk boundary: no credentials, paid data, live trading, or release tag without explicit boundary check.
- Approval lane: autonomous for initial public repo creation/push after Melih delegated the choice; confirmation needed for future release tags or changing license.
- Verification path: completed `uv run pytest`, `uv run ruff check .`, public-data manifest inspection, baseline report inspection, and local git commit check.
