# Validation Protocol

## Purpose

MRPL-017 defines the next validation protocol for Macro Regime Portfolio Lab.

The goal is to stop treating the same full-sample diagnostics as both research
feedback and public evidence. MRPL-016 showed a useful signal, but also found
that the result weakens against a static 60/40 comparator, rolling-window
evidence is uneven, and block-bootstrap Sharpe-difference intervals cross zero.

This protocol is designed for the current monthly sample from 2008 to 2026. It
is intentionally simple enough to implement in the existing Python stack.

## Current Evidence Boundary

Current artifacts are diagnostic:

- the regime definition is transparent and reproducible;
- the feature pipeline is point-in-time approximated with conservative macro
  lagging;
- the walk-forward allocation avoids same-month lookahead;
- robustness checks exist against equal weight and static 60/40.

Current artifacts are not claim-grade:

- regime rules and turnover buffers were reviewed on the same sample used for
  reported performance;
- the strongest sensitivity-grid rows use higher switch buffers than the
  current default;
- static 60/40 has stronger full-sample net Sharpe than the current diagnostic;
- rolling-window evidence is uneven;
- no validation split constrains parameter choice yet.

## Validation Design

Use a two-layer protocol:

1. Locked holdout for public evidence.
2. Nested walk-forward selection inside the non-holdout sample.

This separates research decisions from the period used for final milestone
language.

## Locked Holdout

Use calendar years 2022 through the latest completed evaluation year as the
locked validation period.

With the current data, this means:

- research and calibration window: 2008-05-31 through 2021-12-31;
- locked validation window: 2022-01-31 through 2026-03-31;
- validation rows: 51 monthly signal rows, using the current walk-forward target
  alignment.

Rationale:

- the holdout includes the inflation/hiking cycle where regime awareness should
  plausibly matter;
- it includes the recent 2024-2026 period where the current diagnostic trails
  equal weight;
- it is long enough to be useful but still leaves the earlier sample for
  exploratory rule development;
- it avoids carving out only an easy crisis period.

The validation window must not be used to choose:

- regime definition variants;
- switch-score buffer;
- minimum same-regime history;
- number of selected assets;
- fallback asset;
- benchmark set;
- report language thresholds.

## Nested Selection Rule

Inside the research and calibration window, use expanding walk-forward selection
for any configurable strategy parameter.

Initial candidate grid:

| Parameter | Candidate Values |
| --- | --- |
| switch_score_buffer | 0.00, 0.05, 0.10, 0.20, 0.50 |
| min_regime_history | 12, 24, 36 |
| top_n | 2, 3, 4 |
| fallback_asset | SHY |

Selection objective:

```text
maximize median rolling 36-month Sharpe difference versus the benchmark panel
subject to average monthly turnover <= 0.12
```

Benchmark panel for selection:

- equal-weight ETF universe;
- static SPY/TLT 60/40;
- SHY cash-like defensive proxy.

The selected configuration must be chosen using only data through 2021-12-31.
After selection, freeze the configuration and evaluate it once on the locked
validation window.

## Fixed Before Validation

These are fixed for the first validation run:

- asset universe: SPY, QQQ, IWM, EFA, EEM, TLT, IEF, GLD, DBC, VNQ, UUP, SHY;
- data sources: cached yfinance adjusted prices and FRED/public macro series;
- macro lag rule: one-calendar-month lag for macro-derived features;
- current four-state growth/inflation regime family;
- current stricter growth rule as the default candidate;
- transaction cost convention: 5 bps per one-way turnover;
- validation window start: 2022-01-31;
- benchmark panel listed above.

These can be selected only inside the research window:

- switch-score buffer;
- min_regime_history;
- top_n;
- whether the current default or a pre-declared alternative rule wins the
  research-window selection test.

These require a new protocol note before they can change:

- data vendor or paid data;
- asset universe;
- benchmark panel;
- validation window;
- exact macro release-calendar modeling;
- adding HMM, clustering, or supervised regime models.

## Validation Report Requirements

The validation report should include:

- selected configuration and why it was selected;
- in-sample research-window metrics;
- locked validation-window metrics;
- benchmark panel comparison;
- rolling-window summary inside the validation window when enough months exist;
- stress-period attribution for 2022-2023 and 2024-forward;
- turnover and transaction-cost diagnostics;
- explicit pass/fail interpretation.

Required metrics:

- annualized return;
- annualized volatility;
- Sharpe ratio;
- max drawdown;
- average monthly turnover;
- calendar-year returns;
- Sharpe difference versus each benchmark;
- block-bootstrap uncertainty for validation-window Sharpe differences, labeled
  as a coarse diagnostic.

## Claim Language Rules

Allowed if validation beats all benchmarks on net Sharpe and drawdown is not
worse than the worst benchmark:

- "The locked validation run supports continued research into the transparent
  regime-aware allocation scaffold."
- "The strategy passed the first validation screen against the benchmark panel."

Allowed if validation beats equal weight but not static 60/40:

- "The diagnostic improves on equal weight in the locked validation window but
  does not clear the full benchmark panel."
- "The result remains research-scaffold evidence, not an outperformance claim."

Allowed if validation fails equal weight:

- "The validation protocol rejected the current diagnostic allocation."
- "The repo preserves the pipeline and negative result as part of reproducible
  research."

Never allowed from this milestone:

- "proves outperformance";
- "robust alpha";
- "production strategy";
- "investment-ready";
- "tradeable signal";
- "optimized portfolio";
- "validated macro regime model" without qualification.

## Implementation Plan

MRPL-018 should implement the validation protocol in code:

1. Add a validation configuration module or YAML file with the fixed split and
   candidate grid.
2. Add a script, likely `scripts/run_validation_protocol.py`.
3. Reuse existing walk-forward, sensitivity, benchmark, and robustness helpers.
4. Write machine-readable artifacts under `artifacts/reports/validation_*`.
5. Write `docs/validation-results.md`.
6. Add tests for split boundaries and for "selection uses only pre-2022 rows."

## Decision

Adopt this validation protocol before strengthening public performance language.

Until MRPL-018 is implemented and reviewed, the project should describe the
regime-aware allocation layer as a reproducible diagnostic framework with
promising but unvalidated results.
