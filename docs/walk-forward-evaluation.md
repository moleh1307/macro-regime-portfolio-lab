# Walk-Forward Evaluation Protocol

## Purpose

This protocol defines the first evaluation layer for regime-aware ETF allocation research.
It exists to prevent same-month leakage and premature performance claims.

## Alignment Rule

Each row at month-end `t` contains:

- features and regime label known at or after month-end `t`;
- next-month ETF returns from month-end `t` to month-end `t+1`.

The feature row at `t` must never use realized returns from `t+1`.
The return target for `t` is dropped until `t+1` is a completed month-end, so
partial current-month data cannot enter the evaluation.

## Training Rule

For each signal date, diagnostic allocations use only prior feature rows and
prior next-month returns. The first implementation uses same-regime history:

1. identify the current month-end regime;
2. find earlier rows with the same regime;
3. compute a simple same-regime risk-adjusted score using only those earlier rows;
4. equal-weight the top assets by historical risk-adjusted score;
5. fall back to equal-weight until enough same-regime observations exist.

The default minimum same-regime history is 24 observations.

## Benchmark

The baseline comparison is monthly equal weight across the configured ETF universe.

## Required Output

The evaluation script writes:

- `artifacts/reports/walk_forward_diagnostic.md`
- `artifacts/reports/walk_forward_returns.csv`
- `artifacts/reports/walk_forward_weights.csv`

## Caveats

- This is a protocol diagnostic, not a final strategy.
- Transaction costs, slippage, taxes, liquidity, and exact macro-release calendars
  are not yet modeled.
- Performance differences should not be described as robust or investable until
  later robustness checks are implemented.
