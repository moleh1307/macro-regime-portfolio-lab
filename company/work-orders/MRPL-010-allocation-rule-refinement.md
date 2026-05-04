# MRPL-010 - Refine Diagnostic Allocation Rule

- Owner role: Quant Researcher / Replication QA
- Status: done
- Lifecycle state: Done
- Risk lane: normal
- Canonical artifact: `docs/allocation-rule-review.md`

## Scope

Review and refine the current diagnostic allocation rule before making further performance comparisons:

- inspect concentration and regime-specific asset choices;
- decide whether top-`n` same-regime average return is too naive;
- consider capped weights, defensive sleeves, or volatility-aware ranking;
- keep the result as a diagnostic research rule, not a deployable strategy.

## Acceptance Criteria

- Create a short allocation-rule review document.
- Identify one conservative refinement or explicitly keep the current rule with rationale.
- Add tests if the allocation rule changes.
- Report wording continues to avoid robustness or investment claims.

## Verification Evidence

- Created `docs/allocation-rule-review.md`.
- Replaced raw same-regime average-return ranking with same-regime risk-adjusted ranking: mean next-month return divided by monthly return volatility.
- Preserved conservative top-3 equal-weight selection, 24-observation same-regime minimum, equal-weight warm-up fallback, and SHY fallback when all scores are non-positive.
- Added a unit test showing the ranking penalizes high-volatility assets.
- `uv run pytest`: 15 passed.
- `uv run ruff check .`: all checks passed.
- `uv run python scripts/run_walk_forward.py` completed.
- Updated report wording to describe the risk-adjusted diagnostic rule.
- Result after refinement: regime diagnostic net annualized return 0.0751, volatility 0.1149, Sharpe 0.6534, max drawdown -0.2965; equal-weight net annualized return 0.0669, volatility 0.0970, Sharpe 0.6901, max drawdown -0.2789.
- Average monthly turnover increased to 0.1733 for the regime diagnostic versus 0.0023 for equal weight.

## Blocker / Decision Needed

- None.

## Closeout State

- Done.
