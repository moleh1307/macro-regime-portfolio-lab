# MRPL-007 - Implement Monthly Regime Feature Pipeline

- Owner role: Data Engineer / Research Engineer
- Status: done
- Lifecycle state: Done
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

- `uv run pytest`: 8 passed.
- `uv run ruff check .`: all checks passed.
- `uv run python scripts/build_features.py` completed.
- Feature manifest rows: 216.
- Feature manifest columns: `spy_10m_trend`, `vix_3m_rank`, `cpi_yoy`, `cpi_yoy_3m_change`, `unemployment_3m_change`, `yield_curve_level`, `yield_curve_3m_change`, `fed_funds_3m_change`, `growth_regime`, `inflation_regime`, `regime`.
- Feature date range: 2008-05-31 to 2026-04-30.
- Missing month check: no missing months inside the generated date range.
- Regime counts: improving/easing 99; improving/rising 101; weakening/easing 11; weakening/rising 5.

## Blocker / Decision Needed

- None.

## Closeout State

- Done.
