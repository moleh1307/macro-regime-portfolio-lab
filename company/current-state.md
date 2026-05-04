# Current State

## Capsule

- Objective: Build the reproducible foundation for Macro Regime Portfolio Lab.
- Latest status: MRPL-014 stricter growth regime definition implemented, verified, and pushed.
- Operating mode: build.
- Current milestone: Milestone 2 - first point-in-time regime features and walk-forward evaluation protocol.
- Canonical workspace/repo: `/Users/melihkarakose/Projects/Active/macro-regime-portfolio-lab`; `https://github.com/moleh1307/macro-regime-portfolio-lab`
- Current canonical artifact/output: `artifacts/reports/walk_forward_diagnostic.md`; feature outputs remain generated locally under `data/processed/`.
- Current active workflow: `uv sync`, `uv run pytest`, `uv run python scripts/fetch_data.py`, `uv run python scripts/run_baseline_backtest.py`, `uv run python scripts/build_features.py`, `uv run python scripts/run_walk_forward.py`, `uv run python scripts/run_parameter_sensitivity.py`.
- Known caveats: no outperformance claims should be made from milestone 2; MRPL-014 improved diagnostic metrics, but the result needs post-change robustness review before public-facing performance language is strengthened.
- Latest diagnostic snapshot: stricter growth labels produce 130 improving-growth months and 86 weakening-growth months; default walk-forward net Sharpe is 0.7392 vs equal-weight net Sharpe 0.6901 at 5 bps cost and 0.10 switch-score buffer; sensitivity top setting is buffer 0.50 / 0 bps with strategy net Sharpe 0.9821 vs equal-weight 0.6903.
- Next action: Execute MRPL-015 post-stricter-regime diagnostic review.
- Blockers: none.

## Capability Surface

- Available: filesystem, shell, local git, Python/uv if installed, network access for public data.
- Required now: MRPL-015 post-stricter-regime diagnostic review.
- Missing / uncertain: whether the stronger post-MRPL-014 metrics are robust to parameter choice, sample dependence, and simple allocation-rule assumptions.
- Risk boundary: no credentials, paid data, live trading, or release tag without explicit boundary check.
- Approval lane: autonomous for initial public repo creation/push after Melih delegated the choice; confirmation needed for future release tags or changing license.
- Verification path: completed `uv run pytest`, `uv run ruff check .`, public-data manifest inspection, baseline report inspection, feature manifest inspection, walk-forward report inspection, local git commit check, GitHub repo metadata check, remote tracking check, `git ls-remote` check, milestone 2 planning push verification, MRPL-007 push verification, MRPL-008 push verification, MRPL-009 push verification, MRPL-010 push verification, MRPL-011 push verification, MRPL-012 push verification, MRPL-013 push verification, and MRPL-014 push verification.
