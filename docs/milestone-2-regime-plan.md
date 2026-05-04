# Milestone 2 Plan: First Regime Feature And Evaluation Protocol

## Goal

Milestone 2 should add the first regime-aware research layer without turning the repo into a performance-marketing project.

The milestone is successful if the repo can:

- build a monthly point-in-time feature table from public data;
- define a simple, transparent first regime label;
- run a walk-forward evaluation protocol;
- compare regime-aware allocations against the milestone 1 baseline without overclaiming.

It is not successful if it only adds a complex model that looks impressive but cannot be audited for lookahead bias.

## First Regime Design

Use a transparent four-state regime grid before trying hidden Markov models, clustering, or supervised models.

The first design should classify each month using:

- Growth: improving / weakening
- Inflation: easing / rising

This gives four interpretable regimes:

- improving growth + easing inflation
- improving growth + rising inflation
- weakening growth + easing inflation
- weakening growth + rising inflation

The first implementation should treat this as a research scaffold, not as a final macro model.

## Feature Set V1

Build monthly features from already configured public sources plus ETF prices:

| Feature | Source | Initial definition | Main risk |
| --- | --- | --- | --- |
| Equity trend | SPY adjusted close | price above/below 10-month moving average | market feature can dominate macro interpretation |
| Inflation trend | CPIAUCSL | 12-month CPI inflation and 3-month change | CPI publication lag |
| Labor trend | UNRATE | 3-month change in unemployment rate | monthly release timing |
| Yield curve | T10Y2Y | level and 3-month change | daily series needs monthly alignment |
| Policy rate | FEDFUNDS | level and 3-month change | monthly average vs decision timing |
| Risk stress | VIXCLS | month-end level and 3-month percentile/rank | daily-to-monthly choice |

## Point-In-Time Rule

For milestone 2, features must be shifted so a month-end allocation can only use information that would plausibly have been known at that time.

Initial conservative rule:

- monthly macro features are lagged by one calendar month;
- daily market features can use month-end values only for allocations starting after that month-end;
- labels and allocations must be computed on shifted features, not same-month realized returns.

This rule is intentionally conservative. It can be refined later with exact release calendars.

## Evaluation Protocol

Use a walk-forward protocol before any strategy claim:

1. Build monthly feature matrix and next-month ETF return matrix.
2. Split the sample into expanding windows.
3. Fit or define regimes only using data available up to each rebalance date.
4. Generate next-month allocation weights.
5. Compare against:
   - monthly equal-weight baseline;
   - static 60/40 proxy if added later;
   - cash/SHY defensive proxy when relevant.
6. Report metrics with caveats:
   - annualized return;
   - annualized volatility;
   - Sharpe ratio;
   - max drawdown;
   - turnover;
   - regime counts;
   - years/months covered.

## Acceptance Criteria

Milestone 2 should not be considered complete until:

- feature table generation is reproducible from cached raw data;
- feature table includes a manifest or metadata summary;
- at least one test checks that target returns are forward-looking and features are lagged;
- the report states that the regime design is a first-pass research scaffold;
- strategy comparisons avoid investment-advice language and avoid claiming robustness.

## Deferred

- Hidden Markov models.
- K-means or Gaussian mixture regimes.
- Optimization-heavy allocation.
- Transaction-cost-sensitive conclusions.
- Exact economic-release calendars.
- Live data refreshes or trading/execution.

## Next Implementation Slice

Implement `MRPL-007`:

- create monthly feature engineering module;
- produce `data/processed/monthly_features.csv`;
- write a feature manifest;
- add tests for monthly alignment and lagging.
