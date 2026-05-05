# Fresh-Data-Forward Monitoring

## Purpose

MRPL-024 implements the report scaffold from
`docs/fresh-data-forward-monitoring-protocol.md`.

This is a monitoring scaffold for future completed monthly observations. It is
not a fresh validation result, live trading signal, or outperformance claim.

## Current Status

No completed forward-monitoring return exists in the current cached data. The first monitoring signal is recorded as pending and must wait for a complete next-month price observation.

## Source Boundaries

| source | current_end |
| --- | --- |
| yfinance_adjusted_prices | 2026-05-04 |
| fred_macro_cache | 2026-05-01 |
| monthly_features | 2026-04-30 |

## Monitoring Boundary

| last_inspected_signal | first_monitoring_signal | latest_feature_date | latest_completed_next_return_signal | completed_monitoring_rows | pending_signal_rows | latest_completed_monitoring_signal | latest_pending_signal |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-03-31 | 2026-04-30 | 2026-04-30 | 2026-03-31 | 0 | 1 |  | 2026-04-30 |

## Frozen Rule

| switch_score_buffer | min_regime_history | top_n | max_monthly_turnover | turnover_metric_warmup_months | fallback_asset | cost_bps |
| --- | --- | --- | --- | --- | --- | --- |
| 0.5000 | 12 | 3 | 0.1500 | 12 | SHY | 5.0000 |

## Completed Monitoring Returns

_No rows._

## Pending Signals

| signal_date | regime | selected_assets | strategy_turnover | strategy_cost | status |
| --- | --- | --- | --- | --- | --- |
| 2026-04-30 | improving_growth_rising_inflation | QQQ,SHY,TLT,UUP | 0.0000 | 0.0000 | pending_completed_next_month_return |

## Monitoring Metrics

| monitoring_rows | latest_signal_date | latest_realized_return_date | strategy_cumulative_return | equal_weight_cumulative_return | static_60_40_cumulative_return | shy_cumulative_return | strategy_max_drawdown | average_monthly_turnover | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 |  |  |  |  |  |  |  |  | no_completed_forward_monitoring_returns |

## Warnings

| signal_date | warning | value | threshold | status |
| --- | --- | --- | --- | --- |
| 2026-04-30 | data_freshness_warning | pending_completed_next_month_return | complete_next_month_price_observation | diagnostic_warning |

## Claim Boundary

Allowed language:

- "The monitoring scaffold is ready for future completed monthly observations."
- "The 2026-04-30 signal row is pending a complete next-month return."
- "Monitoring evidence remains diagnostic until enough genuinely new rows
  accumulate."

Not allowed:

- robust outperformance;
- fresh validation;
- live trading signal;
- investment-ready allocation;
- alpha claim.

## Output Tables

- `artifacts/reports/fresh_forward_monitoring_returns.csv`
- `artifacts/reports/fresh_forward_monitoring_metrics.csv`
- `artifacts/reports/fresh_forward_monitoring_warnings.csv`
- `artifacts/reports/fresh_forward_monitoring_pending_signals.csv`
