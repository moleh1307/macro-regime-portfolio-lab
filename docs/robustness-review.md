# Robustness Review

## Purpose

MRPL-016 adds a small robustness review for the post-MRPL-014 regime diagnostic.
This is still a diagnostic research artifact, not an outperformance claim,
investment recommendation, or tuned strategy selection.

## Inputs

- Default diagnostic setting: 0.10 switch-score buffer and 5 bps one-way turnover cost.
- Primary benchmark: monthly equal weight across the ETF universe.
- Additional benchmark: static SPY/TLT 60/40 target weights with the same turnover-cost convention.
- Evaluation rows: 215 signal months in the current walk-forward table.

## Full-Sample Metrics

| strategy | annualized_return | annualized_volatility | sharpe_ratio | max_drawdown |
| --- | --- | --- | --- | --- |
| regime_diagnostic_net | 0.0780 | 0.1055 | 0.7392 | -0.2789 |
| equal_weight_net | 0.0669 | 0.0970 | 0.6901 | -0.2789 |
| static_60_40_net | 0.0859 | 0.1073 | 0.8005 | -0.2622 |

Interpretation: the regime diagnostic beats equal weight on full-sample net
Sharpe, but the static 60/40 benchmark is a harder comparator in this sample.

## Stress Periods

| period | start | end | months | strategy_return | strategy_max_drawdown | equal_weight_return | equal_weight_max_drawdown | static_60_40_return | static_60_40_max_drawdown | strategy_minus_equal_weight | strategy_minus_static_60_40 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gfc_available_sample | 2008-05-31 | 2009-06-30 | 14 | -0.1414 | -0.2789 | -0.1414 | -0.2789 | -0.1254 | -0.2372 | 0.0000 | -0.0160 |
| covid_shock_recovery | 2020-02-29 | 2020-12-31 | 11 | 0.2529 | -0.0281 | 0.1678 | -0.0332 | 0.1628 | -0.0473 | 0.0851 | 0.0901 |
| inflation_hiking_cycle | 2022-01-31 | 2023-12-31 | 24 | 0.1766 | -0.0686 | 0.0022 | -0.1487 | -0.0624 | -0.2069 | 0.1744 | 0.2390 |
| recent_sample | 2024-01-31 | 2026-03-31 | 27 | 0.3005 | -0.0557 | 0.4008 | -0.0319 | 0.2839 | -0.0559 | -0.1002 | 0.0167 |

Interpretation: the default diagnostic's strongest relative result is the
inflation/hiking-cycle period. The recent sample is weaker versus equal weight,
which reinforces that full-sample performance is not broad dominance.

## Rolling 36-Month Windows

| check | value |
| --- | --- |
| 36m windows where strategy Sharpe > equal weight | 86 / 180 |
| 36m windows where strategy Sharpe > static 60/40 | 69 / 180 |
| median strategy minus equal-weight Sharpe | 0.0000 |
| median strategy minus static-60/40 Sharpe | -0.5200 |

Interpretation: rolling windows show uneven evidence. A credible public claim
would need stability across windows, not only a favorable full-sample metric.

## Buffer Subperiod Check

| switch_score_buffer | years_beating_equal_weight | years_beating_static_60_40 | median_vs_equal_weight | median_turnover |
| --- | --- | --- | --- | --- |
| 0.1000 | 8.0000 | 10.0000 | 0.0000 | 0.0833 |
| 0.2000 | 8.0000 | 9.0000 | 0.0000 | 0.0625 |
| 0.5000 | 8.0000 | 9.0000 | 0.0000 | 0.0278 |

Interpretation: higher buffers remain promising, but the result still depends
on a turnover-control parameter. The 0.20 and 0.50 settings should not be
selected as defaults without a pre-declared validation rule.

## Block Bootstrap Sharpe Difference

| strategy_column | benchmark_column | observed_sharpe_difference | bootstrap_mean_difference | bootstrap_p05 | bootstrap_p50 | bootstrap_p95 | share_positive | block_months | samples | seed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| strategy_return_net | equal_weight_return_net | 0.0491 | 0.0549 | -0.1839 | 0.0569 | 0.3069 | 0.6460 | 6 | 1000 | 7 |
| strategy_return_net | static_60_40_return_net | -0.0613 | -0.0633 | -0.4752 | -0.0730 | 0.3516 | 0.4050 | 6 | 1000 | 7 |

Interpretation: the bootstrap is a coarse paired block diagnostic. It is useful
for uncertainty framing, but it is not a formal proof because monthly returns
are serially dependent and the allocation rule was developed on the same sample.

## Decision

The stricter regime diagnostic remains worth developing, but MRPL-016 does not
promote it to a robust outperformance claim. The next methodology step should
separate evaluation from research iteration more explicitly, either with a
pre-registered validation split, a stronger benchmark panel, or a walk-forward
model-selection protocol that prevents choosing parameters from the full grid.

## Output Tables

- `artifacts/reports/robustness_full_sample.csv`
- `artifacts/reports/robustness_subperiods.csv`
- `artifacts/reports/robustness_stress_periods.csv`
- `artifacts/reports/robustness_rolling_windows.csv`
- `artifacts/reports/robustness_buffer_subperiods.csv`
- `artifacts/reports/robustness_bootstrap.csv`
