# Turnover And Cost Sensitivity Review

## Purpose

MRPL-011 reviews whether the diagnostic allocation rule is too sensitive to turnover and simple transaction-cost assumptions.

This is still a research diagnostic. It is not a trading strategy, robustness claim, or investment recommendation.

## Starting Point

After MRPL-010, the diagnostic rule used same-regime risk-adjusted ranking:

- 24 prior same-regime observations required;
- top 3 positive-score assets;
- equal-weight selected assets;
- equal-weight warm-up fallback;
- SHY fallback only when all scores are non-positive.

The post-MRPL-010 diagnostic had higher average turnover than equal weight and lower net Sharpe:

- regime diagnostic average monthly turnover: 0.1733;
- equal-weight average monthly turnover: 0.0023;
- regime diagnostic net Sharpe: 0.6534;
- equal-weight net Sharpe: 0.6901.

## Issue Found

The turnover was lumpy. Most months had no strategy turnover, but basket changes could be large when the selected top assets changed. This is a fragile pattern for a public research repo because it can make apparent performance sensitive to small score-rank changes and cost assumptions.

## Implemented Control

Add a simple switch-score buffer:

```text
keep previous basket unless candidate_score > previous_score * (1 + buffer)
```

Current default:

- `switch_score_buffer = 0.10`

The basket score is the same simple risk-adjusted score used for ranking:

```text
mean(monthly basket return) / volatility(monthly basket return)
```

This is deliberately not an optimizer. It only prevents trading into a similar-scoring basket.

## Why This Is Conservative

- It reduces churn from small rank changes.
- It preserves the transparent top-3 equal-weight basket structure.
- It does not add leverage, shorting, or continuous weight optimization.
- It makes transaction-cost sensitivity visible before further strategy work.

## Remaining Risks

- The 10% buffer is a diagnostic default, not calibrated.
- A buffer can preserve stale allocations in changing regimes.
- Same-regime sample sizes remain small for weakening-growth states.
- Results still need robustness checks across cost assumptions and buffer sizes.

## Decision

Adopt the switch-score buffer as the current diagnostic turnover control. Next useful work should run a small parameter sensitivity grid rather than tuning the buffer to one historical result.

## Observed Result

With the current 10% switch-score buffer:

- average monthly turnover fell from 0.1733 to 0.0314;
- regime diagnostic net Sharpe fell from 0.6534 to 0.5903;
- equal-weight net Sharpe remained 0.6901;
- the diagnostic allocation became more bond/cash-heavy on average.

This is not a performance improvement. It is a useful sensitivity finding: turnover control materially changes the behavior of the diagnostic rule, so the next task should test a small grid of buffer and cost assumptions before adopting any rule as the milestone default.
