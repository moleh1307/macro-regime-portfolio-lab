# Post-Stricter-Regime Diagnostic Review

## Purpose

MRPL-015 reviews the diagnostics after MRPL-014 made the stricter growth regime
definition the active milestone default.

This is a research quality gate, not a performance claim. The goal is to decide
whether the stronger diagnostics are credible enough for limited GitHub
portfolio language, and what must be checked before any stronger public wording.

## Change Reviewed

MRPL-014 changed the growth axis from an OR rule to a both-confirmation rule:

```text
growth = improving if unemployment_3m_change <= 0 AND spy_10m_trend == 1
otherwise weakening
```

Inflation classification remained unchanged:

```text
inflation = easing if cpi_yoy_3m_change <= 0
otherwise rising
```

The updated feature table has 216 monthly observations from 2008-05-31 to
2026-04-30.

## Regime Distribution

The stricter rule materially improves label balance.

| Regime | Months |
| --- | ---: |
| improving_growth_easing_inflation | 59 |
| improving_growth_rising_inflation | 71 |
| weakening_growth_easing_inflation | 51 |
| weakening_growth_rising_inflation | 35 |

Growth-axis totals:

| Growth Label | Months |
| --- | ---: |
| improving_growth | 130 |
| weakening_growth | 86 |

This is a clear methodology improvement over the previous OR rule, which labeled
200 of 216 months as improving growth.

## Default Walk-Forward Result

Default diagnostic settings:

- 24 prior same-regime observations required;
- top 3 positive-score assets;
- 0.10 switch-score buffer;
- 5 bps one-way turnover cost.

| Strategy | Net Annualized Return | Net Volatility | Net Sharpe | Max Drawdown |
| --- | ---: | ---: | ---: | ---: |
| regime_diagnostic_net | 0.0780 | 0.1055 | 0.7392 | -0.2789 |
| equal_weight_net | 0.0669 | 0.0970 | 0.6901 | -0.2789 |

Average monthly turnover:

| Strategy | Turnover |
| --- | ---: |
| regime_diagnostic | 0.1182 |
| equal_weight | 0.0023 |

Interpretation: the default diagnostic now clears equal weight on net Sharpe and
annualized return, but with higher turnover and higher volatility. This is
useful evidence that the refined label definition is worth further research. It
is not yet evidence of robust outperformance.

## Sensitivity Grid Result

The post-change parameter grid has 20 rows: five switch-score buffers by four
transaction-cost assumptions.

Summary by switch-score buffer:

| Switch Buffer | Net Sharpe Range | Best Net Return | Average Turnover |
| ---: | ---: | ---: | ---: |
| 0.00 | 0.6166 to 0.6609 | 0.0772 | 0.1609 |
| 0.05 | 0.5814 to 0.6227 | 0.0720 | 0.1484 |
| 0.10 | 0.7104 to 0.7464 | 0.0788 | 0.1182 |
| 0.20 | 0.8779 to 0.9086 | 0.0811 | 0.0826 |
| 0.50 | 0.9608 to 0.9821 | 0.0877 | 0.0593 |

The top grid row is:

| Switch Buffer | Cost bps | Strategy Net Sharpe | Equal-Weight Net Sharpe | Strategy Turnover |
| ---: | ---: | ---: | ---: | ---: |
| 0.50 | 0.0 | 0.9821 | 0.6903 | 0.0593 |

Twelve of the twenty tested rows beat equal weight on net Sharpe.

Interpretation: the grid is promising but also raises a parameter-dependence
flag. The best historical results occur at 0.20 and 0.50 switch buffers, not at
the current 0.10 default. Those settings trade less and may be preserving
favorable baskets for long stretches. That can be real signal, but it can also
be historical path dependence.

## Calendar-Year Check

Using the default 0.10 buffer and 5 bps cost setting, the strategy beats
equal-weight net return in 8 of 19 calendar years.

Best relative years:

| Year | Strategy Net Return | Equal-Weight Net Return | Difference |
| ---: | ---: | ---: | ---: |
| 2022 | 0.0535 | -0.0518 | 0.1053 |
| 2017 | 0.1918 | 0.1281 | 0.0637 |
| 2023 | 0.1169 | 0.0570 | 0.0599 |
| 2018 | 0.0379 | -0.0085 | 0.0463 |
| 2015 | -0.0313 | -0.0662 | 0.0350 |

Worst relative years:

| Year | Strategy Net Return | Equal-Weight Net Return | Difference |
| ---: | ---: | ---: | ---: |
| 2025 | 0.1042 | 0.1791 | -0.0749 |
| 2014 | 0.0461 | 0.0808 | -0.0347 |
| 2019 | 0.1021 | 0.1255 | -0.0234 |
| 2021 | 0.0694 | 0.0864 | -0.0169 |
| 2026 | 0.0349 | 0.0517 | -0.0168 |

Interpretation: the stronger full-sample metric is not broad yearly dominance.
The default result benefits meaningfully from crisis and tightening-period
behavior, especially 2022. That is plausible for a regime-aware allocation
rule, but it needs subperiod and stress-period validation.

## Regime-Level Check

Default net monthly mean returns by realized signal regime:

| Regime | Months | Strategy Mean | Equal-Weight Mean | Monthly Mean Difference |
| --- | ---: | ---: | ---: | ---: |
| improving_growth_easing_inflation | 59 | 0.0013 | 0.0009 | 0.0004 |
| improving_growth_rising_inflation | 70 | 0.0094 | 0.0078 | 0.0016 |
| weakening_growth_easing_inflation | 51 | 0.0175 | 0.0158 | 0.0017 |
| weakening_growth_rising_inflation | 35 | -0.0051 | -0.0045 | -0.0006 |

Interpretation: the result is not driven by one empty or tiny state, but the
weakening/rising state remains smaller and is still the hardest state for the
simple allocation rule.

## Claim Boundary

Acceptable public language:

- The repo now includes a reproducible point-in-time feature pipeline.
- The repo now includes a walk-forward diagnostic protocol.
- The first transparent regime definition produces more balanced labels after
  review.
- The diagnostic allocation shows promising behavior in the current sample, but
  remains under robustness review.

Avoid:

- claims of outperformance;
- claims that regime-aware allocation works;
- claims that the 0.50 buffer is optimal;
- investment, execution, or production language;
- charts or copy that imply a selected final strategy.

## Main Risks

- Parameter dependence: best grid rows use higher switch buffers than the
  current default.
- Sample dependence: the full-sample result benefits from a small number of
  high-impact relative years.
- Rule dependence: SPY trend is both a regime input and related to risky-asset
  returns.
- Publication timing: macro lagging is conservative but not a full historical
  release-calendar model.
- Benchmark scope: equal-weight is useful but insufficient as the only benchmark.
- Statistical uncertainty: no confidence intervals, bootstrap checks, or
  rolling-window stability diagnostics exist yet.

## Decision

MRPL-014 is a methodology improvement and should remain the current milestone
default.

The stronger post-change diagnostics are credible enough to describe the repo as
having a working, reproducible regime-aware diagnostic framework. They are not
credible enough to claim robust outperformance or select a tuned buffer.

## Recommended Next Task

Before strengthening public performance language, add a robustness review that
tests:

- rolling or expanding subperiod metrics;
- stress-period attribution;
- bootstrap or block-bootstrap uncertainty for Sharpe differences;
- comparison against at least one additional simple benchmark, such as 60/40 or
  risk-parity-style inverse-volatility weights;
- whether the 0.20 and 0.50 switch-buffer rows remain credible outside the
  full-sample grid.
