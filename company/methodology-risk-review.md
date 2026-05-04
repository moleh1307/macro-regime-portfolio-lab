# Methodology Risk Review: Milestone 1

## Confidence Lane

- Baseline pipeline status: verified locally.
- Performance interpretation: working diagnostic only, not a strategy claim.
- Regime-aware allocation status: not implemented yet.

## Reviewed Evidence

- `uv run pytest`: 4 tests passed.
- `uv run ruff check .`: all checks passed.
- `scripts/fetch_data.py`: downloaded yfinance prices and FRED macro series.
- yfinance manifest: 4,864 rows, 12 ETF columns, 2007-01-03 to 2026-05-04.
- FRED manifest: 5,112 rows, 5 macro columns, 2007-01-01 to 2026-05-01.
- `scripts/run_baseline_backtest.py`: generated `artifacts/reports/baseline_equal_weight.md`.

## Risks Found

- Public data can revise or backfill; report comparisons should use cached manifests.
- The baseline omits transaction costs, slippage, taxes, and liquidity constraints.
- Equal-weight monthly rebalancing is only a framework smoke test.
- The current report should not be used to imply regime-aware performance.
- Future release tags still need explicit boundary checks.

## Required Before Stronger Claims

- Add explicit train/test or walk-forward evaluation before any model claims.
- Add lookahead-bias checks when macro features are introduced.
- Version or summarize the exact cached data used for any public result.
- Add transaction-cost assumptions before comparing strategies.

## Milestone 1 Verdict

Milestone 1 is acceptable as a reproducible foundation and baseline diagnostic. It is not acceptable as evidence that a regime-aware allocation strategy works.
