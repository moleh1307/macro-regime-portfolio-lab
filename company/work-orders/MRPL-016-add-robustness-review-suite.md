# MRPL-016 - Add Robustness Review Suite

- Owner role: Quant Researcher / Data Engineer
- Status: done
- Lifecycle state: Completed
- Risk lane: normal
- Canonical artifact: `docs/robustness-review.md`

## Scope

Add a small robustness review for the post-MRPL-014 regime diagnostic before any
public performance language is strengthened.

The goal is not to optimize the strategy. The goal is to test whether the
stronger diagnostic result survives basic robustness checks.

## Acceptance Criteria

- Add subperiod or rolling-window metrics for the default diagnostic setting.
- Add stress-period attribution for major drawdown or macro-regime periods.
- Add a simple uncertainty check for the Sharpe difference, such as bootstrap or
  block-bootstrap diagnostics.
- Add at least one additional simple benchmark beyond equal weight.
- Review whether 0.20 and 0.50 switch-buffer settings remain credible outside a
  full-sample sensitivity ranking.
- Keep conclusions diagnostic and avoid outperformance claims.

## Verification Evidence

- Added `src/macro_regime_portfolio_lab/robustness.py`.
- Added `scripts/run_robustness_review.py`.
- Added tests in `tests/test_robustness.py`.
- Generated `docs/robustness-review.md`.
- Generated robustness tables under `artifacts/reports/`: full sample, subperiods, stress periods, rolling windows, buffer subperiods, and block bootstrap.
- Added static SPY/TLT 60/40 target-weight benchmark with the same turnover-cost convention.
- Full-sample metrics: regime diagnostic net Sharpe 0.7392, equal-weight net Sharpe 0.6901, static 60/40 net Sharpe 0.8005.
- Rolling 36-month windows: strategy Sharpe beats equal weight in 86 of 180 windows and static 60/40 in 69 of 180 windows.
- Block bootstrap Sharpe-difference check: strategy minus equal-weight observed difference 0.0491 with 5th to 95th percentile range -0.1839 to 0.3069; strategy minus static 60/40 observed difference -0.0613 with range -0.4752 to 0.3516.
- Buffer subperiod check: buffers 0.10, 0.20, and 0.50 each beat equal weight in 8 of 19 calendar years.
- `uv run pytest` passed: 22 tests.
- `uv run ruff check .` passed.

## Blocker / Decision Needed

- None.

## Closeout State

- Completed. The robustness suite keeps the result diagnostic and routes next work toward validation protocol design.
