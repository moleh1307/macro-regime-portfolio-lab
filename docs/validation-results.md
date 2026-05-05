# Validation Results

## Purpose

MRPL-018 implements the locked validation protocol from
`docs/validation-protocol.md`.

This report is a diagnostic validation artifact. It is not an investment
recommendation, production strategy, or robust outperformance claim.

## Selected Configuration

| switch_score_buffer | min_regime_history | top_n | fallback_asset | cost_bps |
| --- | --- | --- | --- | --- |
| 0.5000 | 12 | 4 | SHY | 5.0000 |

Selection used only the research/calibration window ending on 2021-12-31. The
locked validation rows starting in 2022 were not available to the parameter
selection step.

## Selection Grid Top Rows

| switch_score_buffer | min_regime_history | top_n | selection_objective | average_strategy_turnover | passes_turnover_constraint | research_start | research_end | research_months | strategy_sharpe | equal_weight_sharpe | static_60_40_sharpe | shy_sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.5000 | 12 | 4 | -0.5394 | 0.0991 | True | 2008-05-31 | 2021-12-31 | 164 | 0.8080 | 0.6466 | 1.0451 | 1.2179 |
| 0.2000 | 24 | 4 | -0.6216 | 0.0447 | True | 2008-05-31 | 2021-12-31 | 164 | 0.7735 | 0.6466 | 1.0451 | 1.2179 |
| 0.5000 | 24 | 4 | -0.6705 | 0.0213 | True | 2008-05-31 | 2021-12-31 | 164 | 0.7314 | 0.6466 | 1.0451 | 1.2179 |
| 0.5000 | 24 | 3 | -0.7325 | 0.0208 | True | 2008-05-31 | 2021-12-31 | 164 | 0.8219 | 0.6466 | 1.0451 | 1.2179 |
| 0.1000 | 24 | 4 | -0.7340 | 0.0610 | True | 2008-05-31 | 2021-12-31 | 164 | 0.7289 | 0.6466 | 1.0451 | 1.2179 |
| 0.1000 | 36 | 4 | -0.7469 | 0.0102 | True | 2008-05-31 | 2021-12-31 | 164 | 0.6845 | 0.6466 | 1.0451 | 1.2179 |
| 0.2000 | 36 | 4 | -0.7469 | 0.0102 | True | 2008-05-31 | 2021-12-31 | 164 | 0.6845 | 0.6466 | 1.0451 | 1.2179 |
| 0.5000 | 36 | 4 | -0.7469 | 0.0102 | True | 2008-05-31 | 2021-12-31 | 164 | 0.6845 | 0.6466 | 1.0451 | 1.2179 |
| 0.0000 | 24 | 4 | -0.8001 | 0.0854 | True | 2008-05-31 | 2021-12-31 | 164 | 0.7434 | 0.6466 | 1.0451 | 1.2179 |
| 0.2000 | 24 | 3 | -0.8354 | 0.0513 | True | 2008-05-31 | 2021-12-31 | 164 | 0.7278 | 0.6466 | 1.0451 | 1.2179 |

The selection objective is the median rolling 36-month Sharpe difference versus
the strongest benchmark in each window, subject to average monthly turnover at
or below 0.12.

## Locked Validation Metrics

| strategy | annualized_return | annualized_volatility | sharpe_ratio | max_drawdown | average_monthly_turnover |
| --- | --- | --- | --- | --- | --- |
| regime_diagnostic_net | 0.1084 | 0.0993 | 1.0911 | -0.1404 | 0.2304 |
| equal_weight_net | 0.0831 | 0.1005 | 0.8266 | -0.1487 | 0.0000 |
| static_60_40_net | 0.0446 | 0.1397 | 0.3194 | -0.2069 |  |
| shy_net | 0.0237 | 0.0214 | 1.1052 | -0.0358 |  |

## Calendar-Year Validation Returns

| period | start | end | months | strategy_return | equal_weight_return | static_60_40_return | shy_return | strategy_minus_equal_weight | strategy_minus_static_60_40 | strategy_minus_shy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2022 | 2022-01-31 | 2022-12-31 | 12 | -0.0515 | -0.0518 | -0.1401 | -0.0246 | 0.0003 | 0.0885 | -0.0269 |
| 2023 | 2023-01-31 | 2023-12-31 | 12 | 0.1809 | 0.0570 | 0.0903 | 0.0369 | 0.1239 | 0.0905 | 0.1440 |
| 2024 | 2024-01-31 | 2024-12-31 | 12 | 0.1753 | 0.1295 | 0.1262 | 0.0398 | 0.0458 | 0.0491 | 0.1356 |
| 2025 | 2025-01-31 | 2025-12-31 | 12 | 0.1345 | 0.1791 | 0.1135 | 0.0477 | -0.0446 | 0.0210 | 0.0868 |
| 2026 | 2026-01-31 | 2026-03-31 | 3 | 0.0370 | 0.0517 | 0.0238 | 0.0025 | -0.0148 | 0.0132 | 0.0344 |

## Validation Stress Periods

| period | start | end | months | strategy_return | strategy_max_drawdown | equal_weight_return | equal_weight_max_drawdown | static_60_40_return | static_60_40_max_drawdown | shy_return | shy_max_drawdown |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| inflation_hiking_cycle | 2022-01-31 | 2023-12-31 | 24 | 0.1200 | -0.1404 | 0.0022 | -0.1487 | -0.0624 | -0.2069 | 0.0114 | -0.0358 |
| recent_sample | 2024-01-31 | 2026-03-31 | 27 | 0.3827 | -0.0562 | 0.4008 | -0.0319 | 0.2839 | -0.0559 | 0.0921 | -0.0062 |

## Block Bootstrap Sharpe Differences

| strategy_column | benchmark_column | observed_sharpe_difference | bootstrap_mean_difference | bootstrap_p05 | bootstrap_p50 | bootstrap_p95 | share_positive | block_months | samples | seed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| strategy_return_net | equal_weight_return_net | 0.2645 | 0.5543 | -0.1193 | 0.5402 | 1.2513 | 0.9190 | 6 | 1000 | 17 |
| strategy_return_net | static_60_40_return_net | 0.7717 | 0.9909 | 0.4477 | 0.9699 | 1.6063 | 1.0000 | 6 | 1000 | 17 |
| strategy_return_net | shy_return_net | -0.0142 | 0.0188 | -0.9220 | 0.0095 | 0.9825 | 0.5120 | 6 | 1000 | 17 |

The bootstrap is a coarse paired block diagnostic. It frames uncertainty around
Sharpe differences, but it does not prove robustness.

## Interpretation

The diagnostic improves on equal weight in the locked validation window but does not clear the full benchmark panel. The result remains research-scaffold evidence, not an outperformance claim.

## Output Tables

- `artifacts/reports/validation_selection_grid.csv`
- `artifacts/reports/validation_returns.csv`
- `artifacts/reports/validation_metrics.csv`
- `artifacts/reports/validation_calendar_years.csv`
- `artifacts/reports/validation_stress_periods.csv`
- `artifacts/reports/validation_bootstrap.csv`
