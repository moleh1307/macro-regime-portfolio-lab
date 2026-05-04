# Allocation Rule Review

## Purpose

MRPL-010 reviews the first diagnostic allocation rule before further comparison work.
The goal is to reduce obvious methodological weakness without turning the project into
an optimized strategy.

## Previous Rule

The previous walk-forward diagnostic selected the top same-regime assets by historical
average next-month return, equal-weighted across the selected assets.

## Issue Found

Raw average-return ranking is too sensitive to noisy high-return assets in small same-regime
samples. It can reward realized jumps without asking whether the return came with high
monthly volatility.

The current output also shows meaningful concentration after warm-up, mostly around QQQ,
SPY, VNQ, and IWM. That concentration is acceptable for a diagnostic, but it should be
earned by a more defensible score than raw average return.

## Refinement

Replace raw same-regime average return ranking with a simple same-regime risk-adjusted
score:

```text
score(asset) = mean(next_month_return) / volatility(next_month_return)
```

The allocation remains deliberately simple:

- require at least 24 prior same-regime observations;
- select the top 3 positive-score assets;
- equal-weight selected assets;
- fall back to equal weight before enough history exists;
- fall back to SHY only if no positive-score asset exists.

This is still a diagnostic research rule, not a final allocation model.

## Why This Is Conservative

- It keeps the rule transparent.
- It avoids portfolio optimization and fitted weights.
- It penalizes unstable same-regime return histories.
- It preserves the existing top-3 concentration cap.
- It does not introduce leverage, shorting, execution, or live-trading assumptions.

## Remaining Risks

- Same-regime samples are still small for weakening-growth states.
- Volatility-aware ranking does not solve macro label quality.
- No transaction-cost sensitivity sweep exists yet.
- No robustness checks exist across alternate feature definitions or sample windows.
- The diagnostic can still look better or worse by chance.

## Decision

Adopt the risk-adjusted same-regime ranking as the current diagnostic allocation rule.
Do not describe the result as robust, investable, or evidence of outperformance.
