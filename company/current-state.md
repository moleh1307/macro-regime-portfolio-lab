# Current State

## Capsule

- Objective: Build the reproducible foundation for Macro Regime Portfolio Lab.
- Latest status: MRPL-017 validation protocol designed, verified, and pushed.
- Operating mode: build.
- Current milestone: Milestone 2 - first point-in-time regime features and walk-forward evaluation protocol.
- Canonical workspace/repo: `/Users/melihkarakose/Projects/Active/macro-regime-portfolio-lab`; `https://github.com/moleh1307/macro-regime-portfolio-lab`
- Current canonical artifact/output: `artifacts/reports/walk_forward_diagnostic.md`; feature outputs remain generated locally under `data/processed/`.
- Current active workflow: `uv sync`, `uv run pytest`, `uv run python scripts/fetch_data.py`, `uv run python scripts/run_baseline_backtest.py`, `uv run python scripts/build_features.py`, `uv run python scripts/run_walk_forward.py`, `uv run python scripts/run_parameter_sensitivity.py`, `uv run python scripts/run_robustness_review.py`.
- Known caveats: no outperformance claims should be made from milestone 2; MRPL-017 defines a locked validation boundary because MRPL-016 found that the default diagnostic beats equal weight full-sample but not static 60/40, rolling-window evidence is uneven, and block-bootstrap Sharpe-difference intervals cross zero.
- Latest validation protocol: research/calibration window is 2008-05-31 through 2021-12-31; locked validation window is 2022-01-31 through 2026-03-31 with current data; validation must compare against equal weight, static SPY/TLT 60/40, and SHY defensive proxy.
- Next action: Execute MRPL-018 validation protocol implementation.
- Blockers: none.

## Capability Surface

- Available: filesystem, shell, local git, Python/uv if installed, network access for public data.
- Required now: MRPL-018 validation protocol implementation.
- Missing / uncertain: whether the locked validation run will preserve any diagnostic edge after parameter selection is constrained to the pre-2022 research window.
- Risk boundary: no credentials, paid data, live trading, or release tag without explicit boundary check.
- Approval lane: autonomous for initial public repo creation/push after Melih delegated the choice; confirmation needed for future release tags or changing license.
- Verification path: completed `uv run pytest`, `uv run ruff check .`, public-data manifest inspection, baseline report inspection, feature manifest inspection, walk-forward report inspection, local git commit check, GitHub repo metadata check, remote tracking check, `git ls-remote` check, milestone 2 planning push verification, MRPL-007 push verification, MRPL-008 push verification, MRPL-009 push verification, MRPL-010 push verification, MRPL-011 push verification, MRPL-012 push verification, MRPL-013 push verification, MRPL-014 push verification, MRPL-015 push verification, MRPL-016 push verification, and MRPL-017 push verification.
