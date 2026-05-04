# MRPL-007 - Implement Monthly Regime Feature Pipeline

- Owner role: Data Engineer / Research Engineer
- Status: ready
- Lifecycle state: Ready
- Risk lane: normal
- Canonical artifact: `data/processed/monthly_features.csv`

## Scope

Implement the first reproducible monthly feature pipeline:

- read cached yfinance prices and FRED macro series;
- resample to monthly observation dates;
- apply conservative macro lag rules from `configs/regime_features.yml`;
- compute V1 features from `docs/milestone-2-regime-plan.md`;
- write `data/processed/monthly_features.csv` and a feature manifest.

## Acceptance Criteria

- Feature script is runnable from CLI.
- Feature output is reproducible from cached raw data.
- Tests cover monthly alignment and lagging behavior.
- Manifest records rows, columns, date range, and lag assumptions.

## Verification Evidence

- Pending.

## Blocker / Decision Needed

- None unless cached raw data is missing or stale.

## Closeout State

- Ready.
