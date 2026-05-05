# Turnover Stability Results

## Purpose

MRPL-021 implements `docs/turnover-stability-protocol.md`.

Report label:

```text
post-holdout-review diagnostic run
```

The 2022-forward period has already been inspected in MRPL-018. This run tests
whether a research-window turnover-stability protocol addresses a known failure
mode, but it is not a fresh independent holdout.

The turnover-stability metrics exclude the configured initial deployment warmup
months from the research-window turnover screen. This prevents the first
portfolio deployment from being treated as recurring allocation instability.

## Selected Configuration

| switch_score_buffer | min_regime_history | top_n | max_monthly_turnover | turnover_metric_warmup_months | fallback_asset | cost_bps |
| --- | --- | --- | --- | --- | --- | --- |
| 0.5000 | 12 | 3 | 0.1500 | 12 | SHY | 5.0000 |

## Candidate Screen

- candidates passing hard turnover-stability thresholds: 24
- candidates rejected before ranking: 48

Top candidate rows:

| switch_score_buffer | min_regime_history | top_n | max_monthly_turnover | turnover_metric_warmup_months | median_rolling_sharpe_difference | turnover_instability_score | allocation_complexity_score | selection_score | passes_turnover_stability | research_start | research_end | research_months | strategy_sharpe | average_turnover | turnover_p90 | turnover_p95 | high_turnover_month_share | turnover_volatility | rolling_12m_average_turnover_max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.5000 | 12 | 3 | 0.1500 | 12 | -0.6642 | 0.2294 | 0.0000 | -0.7789 | True | 2008-05-31 | 2021-12-31 | 164 | 0.6772 | 0.0595 | 0.1500 | 0.1500 | 0.0000 | 0.0721 | 0.1389 |
| 1.0000 | 12 | 3 | 0.1500 | 12 | -0.8512 | 0.2227 | 0.0000 | -0.9625 | True | 2008-05-31 | 2021-12-31 | 164 | 0.6616 | 0.0773 | 0.1500 | 0.1500 | 0.0000 | 0.0740 | 0.1500 |
| 0.7500 | 12 | 3 | 0.1500 | 12 | -0.8591 | 0.2171 | 0.0000 | -0.9677 | True | 2008-05-31 | 2021-12-31 | 164 | 0.6515 | 0.0829 | 0.1500 | 0.1500 | 0.0000 | 0.0734 | 0.1500 |
| 0.2000 | 12 | 3 | 0.1500 | 12 | -0.8925 | 0.2075 | 0.0000 | -0.9962 | True | 2008-05-31 | 2021-12-31 | 164 | 0.6344 | 0.0925 | 0.1500 | 0.1500 | 0.0000 | 0.0718 | 0.1500 |
| 0.2000 | 24 | 3 | 0.1500 | 12 | -0.9414 | 0.2570 | 0.0000 | -1.0699 | True | 2008-05-31 | 2021-12-31 | 164 | 0.6455 | 0.0430 | 0.1500 | 0.1500 | 0.0000 | 0.0668 | 0.1500 |
| 0.5000 | 24 | 3 | 0.1500 | 12 | -0.9414 | 0.2570 | 0.0000 | -1.0699 | True | 2008-05-31 | 2021-12-31 | 164 | 0.6455 | 0.0430 | 0.1500 | 0.1500 | 0.0000 | 0.0668 | 0.1500 |
| 0.7500 | 24 | 3 | 0.1500 | 12 | -0.9414 | 0.2570 | 0.0000 | -1.0699 | True | 2008-05-31 | 2021-12-31 | 164 | 0.6455 | 0.0430 | 0.1500 | 0.1500 | 0.0000 | 0.0668 | 0.1500 |
| 1.0000 | 24 | 3 | 0.1500 | 12 | -0.9414 | 0.2570 | 0.0000 | -1.0699 | True | 2008-05-31 | 2021-12-31 | 164 | 0.6455 | 0.0430 | 0.1500 | 0.1500 | 0.0000 | 0.0668 | 0.1500 |
| 0.2000 | 12 | 2 | 0.1500 | 12 | -0.9849 | 0.2082 | 0.0000 | -1.0890 | True | 2008-05-31 | 2021-12-31 | 164 | 0.5797 | 0.0918 | 0.1500 | 0.1500 | 0.0000 | 0.0719 | 0.1500 |
| 0.5000 | 12 | 2 | 0.1500 | 12 | -0.9829 | 0.2226 | 0.0000 | -1.0941 | True | 2008-05-31 | 2021-12-31 | 164 | 0.5922 | 0.0774 | 0.1500 | 0.1500 | 0.0000 | 0.0738 | 0.1500 |

## Post-Holdout-Review Metrics

| strategy | annualized_return | annualized_volatility | sharpe_ratio | max_drawdown | average_monthly_turnover |
| --- | --- | --- | --- | --- | --- |
| regime_diagnostic_net | 0.0563 | 0.0687 | 0.8194 | -0.1019 | 0.0435 |
| equal_weight_net | 0.0831 | 0.1005 | 0.8266 | -0.1487 | 0.0000 |
| static_60_40_net | 0.0446 | 0.1397 | 0.3194 | -0.2069 |  |
| shy_net | 0.0237 | 0.0214 | 1.1053 | -0.0358 |  |

## Calendar-Year Returns

| period | start | end | months | strategy_return | equal_weight_return | static_60_40_return | shy_return | strategy_minus_equal_weight | strategy_minus_static_60_40 | strategy_minus_shy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2022 | 2022-01-31 | 2022-12-31 | 12 | -0.0659 | -0.0518 | -0.1401 | -0.0246 | -0.0140 | 0.0742 | -0.0413 |
| 2023 | 2023-01-31 | 2023-12-31 | 12 | 0.1595 | 0.0570 | 0.0903 | 0.0369 | 0.1025 | 0.0691 | 0.1226 |
| 2024 | 2024-01-31 | 2024-12-31 | 12 | 0.0773 | 0.1295 | 0.1262 | 0.0398 | -0.0522 | -0.0489 | 0.0375 |
| 2025 | 2025-01-31 | 2025-12-31 | 12 | 0.0552 | 0.1791 | 0.1135 | 0.0477 | -0.1239 | -0.0582 | 0.0075 |
| 2026 | 2026-01-31 | 2026-03-31 | 3 | 0.0252 | 0.0517 | 0.0238 | 0.0025 | -0.0265 | 0.0014 | 0.0227 |

## Stress Periods

| period | start | end | months | strategy_return | strategy_max_drawdown | equal_weight_return | equal_weight_max_drawdown | static_60_40_return | static_60_40_max_drawdown | shy_return | shy_max_drawdown |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| inflation_hiking_cycle | 2022-01-31 | 2023-12-31 | 24 | 0.0831 | -0.1019 | 0.0022 | -0.1487 | -0.0624 | -0.2069 | 0.0114 | -0.0358 |
| recent_sample | 2024-01-31 | 2026-03-31 | 27 | 0.1654 | -0.0357 | 0.4008 | -0.0319 | 0.2839 | -0.0559 | 0.0921 | -0.0062 |

## Bootstrap Sharpe Differences

| strategy_column | benchmark_column | observed_sharpe_difference | bootstrap_mean_difference | bootstrap_p05 | bootstrap_p50 | bootstrap_p95 | share_positive | block_months | samples | seed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| strategy_return_net | equal_weight_return_net | -0.0071 | 0.1983 | -0.4420 | 0.2061 | 0.8301 | 0.6900 | 6 | 1000 | 17 |
| strategy_return_net | static_60_40_return_net | 0.5001 | 0.6349 | 0.1761 | 0.6019 | 1.1751 | 0.9920 | 6 | 1000 | 17 |
| strategy_return_net | shy_return_net | -0.2858 | -0.3372 | -1.2618 | -0.3206 | 0.5044 | 0.2610 | 6 | 1000 | 17 |

## Interpretation

The turnover-stability protocol reduced the known turnover failure mode. Because the 2022-forward period had already been inspected, this remains a post-holdout-review diagnostic, not fresh independent validation.

Do not describe this as robust outperformance, final validation, fresh holdout
evidence, or an investment-ready strategy.

## Output Tables

- `artifacts/reports/turnover_stability_candidate_grid.csv`
- `artifacts/reports/turnover_stability_post_holdout_returns.csv`
- `artifacts/reports/turnover_stability_post_holdout_metrics.csv`
- `artifacts/reports/turnover_stability_calendar_years.csv`
- `artifacts/reports/turnover_stability_stress_periods.csv`
- `artifacts/reports/turnover_stability_bootstrap.csv`
