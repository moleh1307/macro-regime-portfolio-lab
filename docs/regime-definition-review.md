# Regime Definition Review

## Purpose

MRPL-013 reviews whether the current four-state regime definition is strong enough to remain the milestone default.

This is a methodology review, not a performance exercise. The goal is to improve label quality before doing more allocation-rule work.

## Current Definition

The current regime grid has two axes:

- growth: improving / weakening;
- inflation: easing / rising.

Current implementation:

```text
growth = improving if unemployment_3m_change <= 0 OR spy_10m_trend == 1
inflation = easing if cpi_yoy_3m_change <= 0
```

The growth rule is effectively an OR rule because either labor improvement or positive market trend is enough.

## Current Label Distribution

Current feature table:

- rows: 216
- date range: 2008-05-31 to 2026-04-30

Current growth labels:

| Growth Label | Months |
| --- | ---: |
| improving_growth | 200 |
| weakening_growth | 16 |

Current full regime labels:

| Regime | Months |
| --- | ---: |
| improving_growth_easing_inflation | 99 |
| improving_growth_rising_inflation | 101 |
| weakening_growth_easing_inflation | 11 |
| weakening_growth_rising_inflation | 5 |

## Persistence

The current labels have 54 regime transitions across 216 months, for an average run length of 4.0 months.

Longest current runs:

| Regime | Start | End | Months |
| --- | --- | --- | ---: |
| improving_growth_rising_inflation | 2021-02-28 | 2022-08-31 | 19 |
| improving_growth_easing_inflation | 2022-09-30 | 2023-09-30 | 13 |
| improving_growth_easing_inflation | 2011-11-30 | 2012-09-30 | 11 |
| improving_growth_rising_inflation | 2011-01-31 | 2011-10-31 | 10 |
| improving_growth_easing_inflation | 2014-08-31 | 2015-04-30 | 9 |

## Main Issue

The growth axis is too permissive.

Evidence:

- 200 of 216 months are labeled improving growth.
- The label distribution leaves only 16 weakening-growth months for same-regime training.
- The rule can label months as improving growth when one component is clearly weak.
- During COVID, the current rule flips back to improving growth in May 2020 because SPY recovered above its trend while unemployment deterioration was still extreme.
- During the 2021-2023 inflation/hiking period, the rule stays mostly improving growth because labor remained firm even when SPY trend and yield-curve signals were deteriorating.

This is not a fatal flaw for a first scaffold, but it is too weak for the next stage of research.

## Alternative Reviewed

Use a stricter both-confirmation growth rule:

```text
growth = improving if unemployment_3m_change <= 0 AND spy_10m_trend == 1
otherwise weakening
```

This changes 70 labels.

Alternative growth labels:

| Growth Label | Months |
| --- | ---: |
| improving_growth | 130 |
| weakening_growth | 86 |

Alternative full regime labels:

| Regime | Months |
| --- | ---: |
| improving_growth_easing_inflation | 59 |
| improving_growth_rising_inflation | 71 |
| weakening_growth_easing_inflation | 51 |
| weakening_growth_rising_inflation | 35 |

## Historical Period Check

Under the stricter rule:

- GFC period from 2008-06 to 2009-06 is entirely weakening growth, split between rising and easing inflation.
- COVID period from 2020-02 to 2020-12 has a mixed but more plausible sequence, with weakening labels during the shock and some improving labels during the recovery.
- 2021-2023 inflation/hiking period is no longer almost entirely improving growth; it includes weakening/rising and weakening/easing labels.
- Recent 2024-2026 labels are more balanced and do not classify nearly every month as improving.

## Decision

The current OR-based growth definition should not remain the milestone default.

Recommended next implementation:

- change the growth axis to require both labor and market confirmation;
- keep the existing inflation axis for now;
- regenerate monthly features and all downstream reports;
- rerun the parameter sensitivity grid after the label change;
- compare whether regime counts, persistence, and diagnostic results become more credible.

Do not introduce HMMs, clustering, or ML regime models yet. The next step should be a transparent rule refinement.

## Remaining Risks

- A both-confirmation rule may over-label weakening growth during benign market pullbacks.
- SPY trend can still dominate portfolio behavior because it is both a label input and related to asset returns.
- Unemployment has publication lag and revision issues; the current one-month lag is conservative but still approximate.
- Inflation labeling remains binary and may need a neutral/sticky band later.
- Regime quality should be judged by plausibility and stability before strategy performance.
