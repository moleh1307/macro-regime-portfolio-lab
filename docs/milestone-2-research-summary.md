# Milestone 2 Research Summary

## Purpose

Milestone 2 adds the first regime-aware research layer to Macro Regime Portfolio
Lab.

This summary is the public navigation and claim-boundary artifact for the
milestone. It explains what the repo now makes reproducible, what the evidence
suggests, and what it does not prove.

## What Milestone 2 Makes Reproducible

Milestone 2 turns the repo from a baseline data/backtest scaffold into a
transparent regime-aware research workflow:

1. Monthly point-in-time macro and market feature pipeline.
2. Conservative public macro-data lagging rules.
3. Four-state growth/inflation regime labels.
4. Walk-forward allocation diagnostics.
5. Turnover and transaction-cost accounting.
6. Parameter sensitivity and robustness checks.
7. Predeclared validation protocol and first locked validation run.
8. Turnover-stability repair protocol after a validation failure mode.
9. Fresh-data-forward monitoring scaffold for future observations.

The useful outcome is not a final strategy. The useful outcome is an inspectable
research process that keeps data boundaries, parameter selection, diagnostics,
and claim language separated.

## Evidence Arc

### Feature Layer

The first regime feature table uses cached public data and month-end features.
Macro-derived features are shifted by a conservative one-month lag.

The current stricter regime definition uses:

```text
growth = improving if unemployment_3m_change <= 0 AND SPY is above its 10-month average
otherwise weakening
```

and:

```text
inflation = easing if cpi_yoy_3m_change <= 0
otherwise rising
```

This improved the original label balance. The updated feature table has 216
monthly rows from 2008-05-31 to 2026-04-30.

### Walk-Forward Diagnostics

The walk-forward framework evaluates each signal month using only prior
same-regime observations. It records selected assets, returns, turnover, costs,
and benchmark comparisons.

After the stricter regime definition, the default diagnostic beat equal weight
on full-sample net Sharpe, but the evidence was uneven across windows and
subperiods. The robustness review found that static SPY/TLT 60/40 remained a
harder comparator in the full sample.

This is a useful diagnostic result, not an outperformance claim.

### Validation Boundary

MRPL-017 defined a locked validation protocol:

- research/calibration window: 2008-05-31 through 2021-12-31;
- locked validation window: 2022-01-31 through 2026-03-31;
- benchmark panel: equal-weight ETF universe, static SPY/TLT 60/40, and SHY.

MRPL-018 selected parameters using only the research window, then evaluated the
selected rule once in the locked validation window.

The first locked validation run was a partial pass:

| Strategy | Net Sharpe | Max drawdown | Average turnover |
| --- | ---: | ---: | ---: |
| regime_diagnostic_net | 1.0911 | -0.1404 | 0.2304 |
| equal_weight_net | 0.8266 | -0.1487 | 0.0000 |
| static_60_40_net | 0.3194 | -0.2069 | |
| shy_net | 1.1052 | -0.0358 | |

It beat equal weight and static 60/40 on several metrics, but did not clear the
full benchmark panel because SHY had slightly higher Sharpe and much lower
drawdown. It also revealed a turnover failure mode: the selected rule's
2022-forward average monthly turnover rose to 0.2304.

### Turnover-Stability Repair

MRPL-020 through MRPL-022 addressed that failure mode without pretending the
2022-forward period was fresh again.

MRPL-021 selected a turnover-stable second-cycle branch:

| Parameter | Value |
| --- | ---: |
| switch_score_buffer | 0.50 |
| min_regime_history | 12 |
| top_n | 3 |
| max_monthly_turnover | 0.15 |
| turnover_metric_warmup_months | 12 |
| fallback_asset | SHY |
| cost_bps | 5.0 |

This reduced the inspected 2022-forward average monthly turnover from 0.2304 to
0.0435.

It did not strengthen the performance evidence. In the same inspected period,
the turnover-stable branch had net Sharpe 0.8194 versus equal weight 0.8266 and
SHY 1.1052. The correct interpretation is narrow: the branch reduced the known
turnover failure mode and is a better research default for future monitoring.

### Fresh Forward Monitoring

MRPL-023 and MRPL-024 created a forward-monitoring protocol and scaffold.

Current boundary:

| Item | Date / Count |
| --- | ---: |
| last already-inspected realized signal row | 2026-03-31 |
| first forward-monitoring signal row | 2026-04-30 |
| completed forward-monitoring returns | 0 |
| pending signal rows | 1 |

The scaffold records the 2026-04-30 signal as pending and waits for complete May
2026 month-end prices before recording a realized forward-monitoring return.
Partial May data is not treated as forward evidence.

## What The Repo Can Claim

Allowed public claims:

- The repo implements a reproducible public-data research pipeline for
  regime-aware ETF allocation.
- The repo includes point-in-time feature construction, walk-forward evaluation,
  transaction-cost accounting, validation boundaries, robustness checks, and
  forward-monitoring scaffolding.
- The first locked validation run was a partial pass that beat equal weight but
  did not clear the full benchmark panel.
- The turnover-stable branch reduced a known turnover failure mode and is now
  the current research branch for future monitoring.
- The evidence remains diagnostic and requires genuinely new forward data.

## What The Repo Must Not Claim

Do not describe the project as:

- robust outperformance;
- validated strategy;
- investment-ready allocation;
- live trading system;
- alpha model;
- production portfolio optimizer;
- fresh validation after the post-holdout-review cycle.

The strongest credible statement is that milestone 2 builds a serious
reproducible research process and preserves negative or partial evidence rather
than hiding it.

## Repository Hygiene Review

Current strengths:

- CLI scripts reproduce the main artifacts.
- Tests cover core backtest, features, validation splits, turnover-stability
  selection, and fresh-forward monitoring boundaries.
- Generated report tables are stored under `artifacts/reports/`.
- Cached raw and processed data remain gitignored by default.
- Source manifests record data boundaries.
- README links the main methodology artifacts.

Remaining hygiene opportunities before a broader public polish pass:

- Add a compact docs index if the docs folder keeps growing.
- Consider a single milestone status badge/table in the README.
- Add a short "how to read results" section for non-quant GitHub readers.
- Consider notebook examples only after the scripted workflow remains the source
  of truth.

None of these are blockers. The repo is already credible as a GitHub portfolio
artifact for process quality and quant research discipline.

## Decision

Milestone 2 is coherent enough to present publicly as a reproducible research
milestone, provided the README and docs keep the current claim boundary.

The next useful work should be light public-facing polish, not more methodology
machinery: make the repo easier to scan without weakening the diagnostic framing.
