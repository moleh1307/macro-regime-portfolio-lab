# Current State

## Capsule

- Objective: Build the reproducible foundation for Macro Regime Portfolio Lab.
- Latest status: Initial standalone repo scaffold, public-data cache, baseline backtest, and methodology risk review completed locally.
- Operating mode: build.
- Current milestone: Milestone 1 - public-data cache, custom baseline backtester, one baseline report.
- Canonical workspace/repo: `/Users/melihkarakose/Projects/Active/macro-regime-portfolio-lab`
- Current canonical artifact/output: `artifacts/reports/baseline_equal_weight.md`; data manifests are in ignored raw-data cache folders.
- Current active workflow: `uv sync`, `uv run pytest`, `uv run python scripts/fetch_data.py`, `uv run python scripts/run_baseline_backtest.py`.
- Known caveats: GitHub remote not created yet; license is TBD before public release; no outperformance claims should be made in milestone 1.
- Next action: Initialize local git baseline, then decide whether to create/push the public GitHub repo.
- Blockers: none for local setup; public GitHub creation/push requires a later release/GitHub boundary check.

## Capability Surface

- Available: filesystem, shell, local git, Python/uv if installed, network access for public data.
- Required now: local git baseline and GitHub launch decision.
- Missing / uncertain: GitHub remote creation status; exact future license choice.
- Risk boundary: no credentials, paid data, live trading, or public release without explicit boundary check.
- Approval lane: autonomous for local repo setup and public-data pulls; confirmation needed before public release/tag or changing license.
- Verification path: completed `uv run pytest`, `uv run ruff check .`, public-data manifest inspection, and baseline report inspection.
