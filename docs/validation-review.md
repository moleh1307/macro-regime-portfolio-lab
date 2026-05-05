# Validation Review

## Purpose

MRPL-019 reviews the locked validation results from MRPL-018 and decides the
next methodology direction.

This is a claim-boundary review. It does not tune the current result, select a
new strategy, or convert the validation run into a performance claim.

## Validation Result Summary

MRPL-018 selected this configuration using only data through 2021-12-31:

| Parameter | Selected Value |
| --- | ---: |
| switch_score_buffer | 0.50 |
| min_regime_history | 12 |
| top_n | 4 |
| fallback_asset | SHY |
| cost_bps | 5.0 |

Locked validation window:

- start: 2022-01-31;
- end: 2026-03-31;
- rows: 51 monthly signal rows.

Locked validation metrics:

| Strategy | Net Annualized Return | Net Volatility | Net Sharpe | Max Drawdown | Average Turnover |
| --- | ---: | ---: | ---: | ---: | ---: |
| regime_diagnostic_net | 0.1084 | 0.0993 | 1.0911 | -0.1404 | 0.2304 |
| equal_weight_net | 0.0831 | 0.1005 | 0.8266 | -0.1487 | 0.0000 |
| static_60_40_net | 0.0446 | 0.1397 | 0.3194 | -0.2069 | |
| shy_net | 0.0237 | 0.0214 | 1.1052 | -0.0358 | |

## Protocol Outcome

Under `docs/validation-protocol.md`, this is a partial pass.

What passed:

- parameter selection used only the pre-2022 research/calibration window;
- the locked validation run beats equal weight on net annualized return, net
  Sharpe, and max drawdown;
- the locked validation run beats static 60/40 on net annualized return, net
  Sharpe, and max drawdown;
- validation artifacts are reproducible from the CLI workflow.

What failed:

- the strategy does not clear the full benchmark panel because SHY has slightly
  higher validation Sharpe and much lower drawdown;
- the selected configuration has high validation turnover at 0.2304 average
  monthly turnover;
- the bootstrap Sharpe difference versus SHY is effectively inconclusive:
  observed difference -0.0142 with 5th to 95th percentile range -0.9220 to
  0.9825;
- 2025 and the partial 2026 sample trail equal weight.

## Why This Is Not Claim-Grade

The result is useful but not public-performance-grade.

Reasons:

- the strategy clears equal weight but not the full benchmark panel;
- SHY is not a perfect "strategy benchmark," but it is a valid defensive hurdle
  for a regime-aware allocation that can rotate defensively;
- the selected rule's validation turnover is much higher than its
  research-window turnover, which suggests unstable allocation behavior in the
  locked period;
- the validation sample is only 51 monthly rows, so small return sequences can
  dominate Sharpe comparisons;
- using the current validation result to immediately choose a new parameter
  would leak information from the holdout into the research process.

Acceptable public framing remains:

- "The locked validation run beats equal weight but does not clear the full
  benchmark panel."
- "The evidence remains diagnostic and motivates further methodology work."

Not acceptable:

- robust outperformance;
- validated strategy;
- tradeable signal;
- optimized allocation;
- alpha claim.

## Turnover Review

The most actionable failure is turnover.

The selected rule satisfied the research-window turnover constraint:

- research-window average monthly turnover: 0.0991;
- allowed maximum: 0.12.

But in validation:

- validation average monthly turnover: 0.2304.

This is a material regime-shift warning. The selected configuration did not
generalize its turnover behavior into the locked window. A public research repo
should treat that as a methodology defect, not as a minor transaction-cost
detail.

The next methodology step should not simply tighten the switch buffer based on
the validation outcome. That would tune to the holdout. Instead, the project
should improve the selection protocol so future candidate rules are rejected
when their turnover is unstable inside the research window.

## Methodology Decision

Priority order after MRPL-019:

1. Allocation-rule simplicity and turnover stability.
2. Benchmark panel clarity.
3. Regime definition refinements.

Rationale:

- benchmark panel refinement is not the main issue; SHY exposed a real defensive
  hurdle that should remain visible;
- regime definition work can wait because the current labels are already much
  more balanced than the original OR rule;
- allocation turnover instability is the immediate behavior defect revealed by
  validation;
- a simpler allocation rule or stricter research-window turnover-stability
  screen is the cleanest next step without using validation to tune directly.

## Recommended Next Task

MRPL-020 should design a second-cycle validation protocol focused on turnover
stability and allocation-rule simplicity.

Requirements for that task:

- do not change the MRPL-018 locked validation result;
- preserve the MRPL-018 partial-pass evidence in public docs;
- define turnover-stability diagnostics using only the research window;
- consider simpler candidate allocation rules, such as:
  - top-2 or top-3 only;
  - max-change-per-month guard;
  - stay-in-basket unless replacement clears a larger predeclared margin;
  - defensive sleeve cap rather than full defensive rotation;
- define whether a second locked validation attempt is allowed and how it should
  be labeled to avoid pretending the holdout is fresh.

## Decision

Do not strengthen public performance language.

Keep the result as a credible partial validation of the research scaffold: it
beats equal weight in the locked window, but it fails the full benchmark panel
and reveals turnover instability. The next work should address allocation-rule
simplicity and turnover stability before further regime modeling.
