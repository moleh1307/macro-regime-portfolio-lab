# Walk-Forward Regime Evaluation Diagnostic

## Purpose

This report verifies the walk-forward evaluation protocol. It is a diagnostic
research scaffold, not a robustness claim, investment recommendation, or live
allocation system.

## Method

- Signal date: month end.
- Target return: next-month ETF return, aligned to the signal month.
- Training rule: each signal uses only earlier rows with the same regime label.
- Diagnostic allocation: top historical same-regime assets by average next-month
  return, equal-weighted, with equal-weight fallback until enough same-regime
  observations exist.
- Benchmark: monthly equal weight across the configured ETF universe.
- Transaction costs: not modeled.
- Evaluation period: 2008-05-31 to 2026-03-31.

## Metrics

| Strategy | Metric | Value |
| --- | --- | ---: |
| regime_diagnostic | Annualized Return | 0.0941 |
| regime_diagnostic | Annualized Volatility | 0.1391 |
| regime_diagnostic | Sharpe Ratio | 0.6764 |
| regime_diagnostic | Max Drawdown | -0.2804 |
| equal_weight | Annualized Return | 0.0669 |
| equal_weight | Annualized Volatility | 0.0970 |
| equal_weight | Sharpe Ratio | 0.6903 |
| equal_weight | Max Drawdown | -0.2789 |

## Regime Counts

| Regime | Months |
| --- | ---: |
| improving_growth_easing_inflation | 99 |
| improving_growth_rising_inflation | 100 |
| weakening_growth_easing_inflation | 11 |
| weakening_growth_rising_inflation | 5 |

## Caveats

- This protocol is designed to catch alignment and leakage problems before
  stronger strategy research.
- The diagnostic allocation is intentionally simple and should not be treated as
  a final investment model.
- It does not include transaction costs, slippage, taxes, liquidity limits, or
  exact macro-release calendars.
- Any apparent performance difference requires further robustness checks before
  being used in public claims.
