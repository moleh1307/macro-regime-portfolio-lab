# Turnover Stability Protocol

## Purpose

MRPL-020 defines the second-cycle methodology protocol after MRPL-019 reviewed
the first locked validation result.

MRPL-018 is preserved as a partial validation result:

- the selected rule beat equal weight in the locked 2022-forward window;
- it did not clear the full benchmark panel because SHY had slightly higher
  Sharpe and much lower drawdown;
- it revealed turnover instability, with average monthly turnover rising from
  0.0991 in the research window to 0.2304 in validation.

This protocol does not tune directly to that validation outcome. It defines
research-window-only diagnostics and simpler allocation-rule candidates for the
next cycle.

## Evidence Boundary

The 2022-forward validation window has already been inspected.

Therefore, any future run on that same window must be labeled:

```text
post-holdout-review diagnostic
```

It must not be called:

- fresh holdout;
- independent validation;
- final validation;
- proof of outperformance;
- production-ready result.

MRPL-018 remains the first locked validation result. It should not be overwritten
or reframed as if it never happened.

## Problem To Solve

The immediate methodology defect is not that the strategy failed to beat every
benchmark. The immediate defect is that the selected rule's turnover behavior
did not generalize.

Research-window selection constraint:

```text
average monthly turnover <= 0.12
```

Observed result:

| Window | Average Monthly Turnover |
| --- | ---: |
| research/calibration | 0.0991 |
| locked validation | 0.2304 |

This means average turnover alone is not a sufficient research-window screen.
The next cycle needs diagnostics that penalize unstable or clustered turnover
inside the research window before any 2022-forward post-holdout-review run.

## Research-Window Diagnostics

Use only rows through 2021-12-31 for second-cycle selection.

Required turnover-stability diagnostics:

| Diagnostic | Definition | Initial Threshold |
| --- | --- | ---: |
| average turnover | mean monthly strategy turnover | <= 0.10 |
| turnover p90 | 90th percentile monthly strategy turnover | <= 0.35 |
| turnover p95 | 95th percentile monthly strategy turnover | <= 0.50 |
| high-turnover month share | share of months with turnover > 0.25 | <= 0.20 |
| turnover volatility | standard deviation of monthly turnover | <= 0.18 |
| rolling turnover max | max 12-month rolling average turnover | <= 0.18 |

Candidate rules failing any hard threshold should be rejected before ranking.

The thresholds are deliberately conservative and should be reviewed only inside
the research window. They should not be adjusted to make the MRPL-018 validation
period look better.

## Second-Cycle Selection Objective

For candidates that pass hard turnover-stability thresholds, rank by:

```text
median rolling 36-month Sharpe difference versus best benchmark
- 0.50 * turnover_instability_score
- 0.25 * allocation_complexity_score
```

Where:

```text
turnover_instability_score =
    turnover_p90
    + high_turnover_month_share
    + max(0, rolling_12m_average_turnover_max - average_turnover)
```

And:

```text
allocation_complexity_score =
    0.00 for fixed equal-weight baskets with top_n <= 3
    0.10 for top_n = 4
    0.20 for any rule with dynamic defensive sleeve caps
```

Interpretation:

- risk-adjusted performance still matters;
- unstable turnover is penalized before it reaches validation;
- simpler allocation rules are preferred when diagnostics are close.

## Candidate Rule Families

Second-cycle candidates should be simple. Do not introduce optimization-heavy
allocation or machine-learning regimes yet.

Allowed candidates:

| Family | Description | Reason To Test |
| --- | --- | --- |
| top-2 basket | equal-weight top two positive-score assets | lower churn and simpler exposure |
| top-3 basket | equal-weight top three positive-score assets | close to current rule but less broad than top-4 |
| stricter replacement margin | keep previous basket unless candidate score beats previous by a larger predeclared margin | directly targets churn |
| max monthly turnover guard | cap effective basket change per rebalance | tests turnover stability without changing labels |
| defensive sleeve cap | cap SHY/defensive exposure rather than allowing full defensive fallback | avoids all-or-nothing defensive rotation |

Disallowed for this cycle:

- HMMs or clustering;
- supervised return prediction;
- continuous mean-variance optimization;
- leverage or shorting;
- tuning rules directly on 2022-forward validation behavior.

## Benchmark Panel

Keep the benchmark panel unchanged for the second cycle:

- equal-weight ETF universe;
- static SPY/TLT 60/40;
- SHY defensive proxy.

Rationale:

- changing the benchmark panel now would weaken the validation discipline;
- SHY exposed a real defensive hurdle, even if it is not a complete strategy
  benchmark;
- benchmark refinement can happen later as a separate task.

## Second Validation Labeling

If MRPL-021 implements this protocol and reruns 2022-forward data, its report
must use this label:

```text
post-holdout-review diagnostic run
```

Required caveat:

```text
The 2022-forward period has already been inspected in MRPL-018. This run tests
whether a research-window turnover-stability protocol addresses a known failure
mode, but it is not a fresh independent holdout.
```

Acceptable conclusions:

- "The turnover-stability protocol reduced the known turnover failure mode."
- "The second-cycle diagnostic remains partial and requires future fresh data."
- "The second-cycle protocol did not improve turnover stability."

Not acceptable:

- "validated on holdout";
- "new independent validation";
- "robust outperformance";
- "strategy fixed";
- "investment-ready."

## Implementation Requirements

MRPL-021 should implement:

- turnover-stability metrics in a reusable module;
- second-cycle candidate grid under configuration;
- research-window-only selection with hard turnover-stability filters;
- post-holdout-review output artifacts under
  `artifacts/reports/turnover_stability_*`;
- `docs/turnover-stability-results.md`;
- tests proving:
  - turnover diagnostics use only research-window rows;
  - 2022-forward rows are excluded from candidate selection;
  - rejected candidates cannot be selected even with stronger Sharpe;
  - output reports carry the post-holdout-review label.

## Decision

Adopt turnover stability as the next methodology gate.

Do not change the regime definition, benchmark panel, or public claim language
until a second-cycle protocol has tested whether simpler allocation and stricter
research-window turnover diagnostics reduce the failure mode revealed by
MRPL-018.
