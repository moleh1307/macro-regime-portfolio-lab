# Fresh-Data-Forward Monitoring Protocol

## Purpose

MRPL-023 defines how Macro Regime Portfolio Lab should monitor genuinely new
monthly data after the already-inspected sample.

The goal is not to create another backtest split. The goal is to preserve a
clean boundary between:

- historical research and post-holdout-review diagnostics already inspected;
- future monthly observations that arrive after the current data snapshot.

## Current Data Boundary

The current local data snapshot was generated on 2026-05-04.

Observed source boundaries:

| Source | Current end |
| --- | ---: |
| yfinance adjusted prices | 2026-05-04 |
| FRED/public macro cache | 2026-05-01 |
| monthly feature table | 2026-04-30 |
| turnover-stability realized return table | 2026-03-31 signal row |

The 2026-04-30 feature row exists, but the next-month return for that signal was
not complete in the current cache because May 2026 had only partial price data.

Forward monitoring therefore starts with the 2026-04-30 signal row, but the
first realized monitoring return should be recorded only after a complete May
2026 month-end price observation is available.

Practical boundary:

- last already-inspected realized signal row: 2026-03-31;
- first forward-monitoring signal row: 2026-04-30;
- first forward-monitoring realized return: 2026-04-30 signal evaluated over
  the following completed month.

Do not backfill newly fetched data into the MRPL-018 or MRPL-021 interpretation
as if it were part of the original validation evidence.

## Frozen Monitoring Rule

Use the MRPL-021 turnover-stable branch as the frozen monitoring rule.

Configuration:

| Parameter | Frozen value |
| --- | ---: |
| switch_score_buffer | 0.50 |
| min_regime_history | 12 |
| top_n | 3 |
| max_monthly_turnover | 0.15 |
| turnover_metric_warmup_months | 12 |
| fallback_asset | SHY |
| cost_bps | 5.0 |

Benchmark panel:

- equal-weight ETF universe net of the same turnover-cost convention;
- static SPY/TLT 60/40 net of the same turnover-cost convention;
- SHY defensive proxy.

The monitoring rule may recompute trailing regime histories as time advances,
because that is how the walk-forward rule operates. It must not change the
frozen configuration in response to the monitoring results.

## Monthly Monitoring Workflow

For each completed new month:

1. Refresh public data with the existing free-data pipeline.
2. Rebuild monthly features with the existing point-in-time lag rules.
3. Run the frozen turnover-stable branch through the new completed signal row.
4. Append only new monitoring rows to a monitoring artifact.
5. Record the source snapshot date and latest source manifest boundaries.
6. Do not change the selected parameters or thresholds inside the monitoring
   artifact.

The monitoring report should track:

- signal date;
- realized next-month strategy net return;
- benchmark net returns;
- selected regime;
- selected assets or final target weights;
- monthly strategy turnover;
- transaction-cost drag;
- cumulative strategy and benchmark returns since monitoring start;
- strategy minus each benchmark since monitoring start;
- max drawdown since monitoring start;
- rolling average turnover once enough monitoring months exist;
- any rule warnings triggered that month.

## Warning Rules

Warnings are diagnostics, not automatic reasons to change the rule.

Initial warning thresholds:

| Warning | Trigger |
| --- | --- |
| turnover spike | monthly turnover > 0.15 after the cap is applied |
| turnover drift | 6-month average turnover > 0.10 after at least 6 monitoring rows |
| drawdown warning | monitoring-period strategy drawdown worse than -0.15 |
| equal-weight lag | strategy trails equal weight by more than 10 percentage points cumulatively |
| defensive lag | strategy trails SHY by more than 10 percentage points cumulatively |
| repeated benchmark lag | strategy trails both equal weight and SHY over 6 consecutive monitoring rows |
| data freshness warning | source manifests do not include a completed month needed for the latest signal return |

Warnings should be preserved in the monitoring log. They should not trigger
parameter edits without a separate methodology review work order.

## Evidence Handling

Monitoring evidence should be classified as follows:

| Evidence type | Treatment |
| --- | --- |
| first 1-5 monitoring rows | anecdotal forward observations |
| 6-11 monitoring rows | early monitoring evidence, still too small for claims |
| 12+ monitoring rows | useful forward-monitoring sample, still not a proof of robustness |
| warning-free period | evidence that the rule behaved as specified, not outperformance evidence |
| warning-triggered period | evidence for a future methodology review, not immediate tuning authority |

Fresh monitoring rows can strengthen confidence in process discipline before
they strengthen confidence in returns. The monitoring protocol is primarily an
anti-leakage device.

## Allowed Report Language

Allowed:

- "The frozen turnover-stable branch has been monitored on newly arriving data
  since the 2026-04-30 signal row."
- "The monitoring log records forward observations after the already-inspected
  MRPL-018 and MRPL-021 samples."
- "Monitoring evidence remains early and diagnostic."
- "A warning was triggered and should be reviewed without changing the frozen
  rule inside the monitoring report."

Not allowed:

- fresh validation, unless a later protocol explicitly defines a new validation
  design before enough forward data accumulates;
- robust outperformance;
- live trading signal;
- investment-ready allocation;
- alpha claim;
- parameter improvement based on the monitoring rows without a separate
  methodology review.

## Artifact Requirements For Implementation

The implementation should create separate monitoring artifacts rather than
overwriting validation or turnover-stability outputs.

Recommended paths:

- `artifacts/reports/fresh_forward_monitoring_returns.csv`
- `artifacts/reports/fresh_forward_monitoring_metrics.csv`
- `artifacts/reports/fresh_forward_monitoring_warnings.csv`
- `docs/fresh-data-forward-monitoring.md`

The report should include the frozen configuration, data snapshot boundary, row
count, latest signal date, latest realized return date, warnings, and caveats.

## Decision

Use the MRPL-021 turnover-stable branch as the frozen research default for
fresh-data-forward monitoring.

The first monitoring signal row is 2026-04-30. Its realized return should not be
recorded until a complete May 2026 month-end price observation is available.

Future monitoring should preserve new data as evidence, not use it as authority
to tune the current branch.
