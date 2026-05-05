# Macro Regime Portfolio Lab

Reproducible quant research repo for regime-aware ETF allocation using free public data.

The first milestone is intentionally modest: build a reliable data pipeline and baseline backtest framework, then produce one simple report. This repo should not claim outperformance until the data, assumptions, and evaluation protocol are solid.

## Scope

- Free public data only by default.
- No API keys required for the baseline pipeline.
- Research and backtesting only.
- No live trading, execution, broker integration, or investment advice.
- Initial ETF universe: SPY, QQQ, IWM, EFA, EEM, TLT, IEF, GLD, DBC, VNQ, UUP, SHY.

## Stack

- Python with `uv`
- `pandas` first
- `scikit-learn` and `statsmodels` for later regime models
- Simple custom backtester for milestone 1
- Notebooks for exploration, scripts for reproducible runs

## Repository Layout

```text
configs/        Asset universe and data source configuration
data/           Cached raw/interim/processed data, not committed by default
artifacts/      Generated reports, charts, and tables
notebooks/      Exploratory notebooks
scripts/        Reproducible CLI entry points
src/            Importable Python package
tests/          Local unit tests
company/        Minimal JARVIS Specialist project state
```

## Quick Start

```bash
uv sync
uv run pytest
uv run python scripts/fetch_data.py
uv run python scripts/run_baseline_backtest.py
uv run python scripts/build_features.py
uv run python scripts/run_walk_forward.py
uv run python scripts/run_robustness_review.py
uv run python scripts/run_validation_protocol.py
```

The baseline scripts write cached public data under `data/raw/` and a simple report under `artifacts/reports/`.
The feature script writes the monthly point-in-time feature table under `data/processed/`.
The walk-forward script writes diagnostic evaluation artifacts under `artifacts/reports/`.

## Milestone 1

Build the reproducible foundation:

- Download and cache ETF price data from Yahoo Finance via `yfinance`.
- Download and cache selected macro series from FRED/public sources.
- Write source manifests for downloaded data.
- Run a simple monthly rebalanced equal-weight ETF baseline.
- Generate a baseline markdown report with assumptions, metrics, and caveats.

Outperformance, model selection, and regime-aware allocation are deliberately deferred until milestone 2+.

## Milestone 2 Direction

The next milestone adds the first regime-aware research layer:

- monthly point-in-time macro/market feature table;
- conservative lag rules for public macro data;
- transparent four-state growth/inflation regime grid;
- walk-forward evaluation protocol before any strategy claims.

See [Milestone 2 Plan](docs/milestone-2-regime-plan.md).

The current feature pipeline produces `data/processed/monthly_features.csv` and a matching manifest from cached raw data.
The current walk-forward pipeline produces a diagnostic report and aligned return/weight tables. It is a protocol check, not a robustness claim.

The current regime diagnostic review is in [Post-Stricter-Regime Diagnostic Review](docs/post-stricter-regime-diagnostic-review.md), with follow-up robustness checks in [Robustness Review](docs/robustness-review.md). The evidence boundary is defined in [Validation Protocol](docs/validation-protocol.md), the first locked validation run is in [Validation Results](docs/validation-results.md), and the interpretation is in [Validation Review](docs/validation-review.md). These artifacts treat the strategy evidence as promising research scaffolding, not a robust outperformance claim.

## License

MIT License.
