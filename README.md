# Macro Regime Portfolio Lab

Reproducible quant research repo for regime-aware ETF allocation using free
public data.

The goal is research credibility: public data, reproducible scripts, explicit
data boundaries, and careful claim discipline. This repo is not a trading system
and does not claim robust outperformance.

## Current Status

| Area | Status | Where to Read |
| --- | --- | --- |
| Public-data pipeline | Reproducible ETF and macro caches with source manifests | `scripts/fetch_data.py` |
| Baseline backtest | Equal-weight ETF baseline report | `scripts/run_baseline_backtest.py` |
| Regime features | Monthly point-in-time growth/inflation regime table | [Milestone 2 Plan](docs/milestone-2-regime-plan.md) |
| Walk-forward diagnostics | Regime-aware allocation diagnostics with costs and turnover | [Walk-Forward Evaluation](docs/walk-forward-evaluation.md) |
| Robustness review | Subperiod, rolling-window, bootstrap, and benchmark checks | [Robustness Review](docs/robustness-review.md) |
| Locked validation | First predeclared validation run, partial pass only | [Validation Results](docs/validation-results.md) |
| Turnover stability | Second-cycle repair of a turnover failure mode | [Turnover Stability Review](docs/turnover-stability-review.md) |
| Fresh forward monitoring | Scaffold ready; first signal is pending completed next-month data | [Fresh-Data-Forward Monitoring](docs/fresh-data-forward-monitoring.md) |

For the milestone-level interpretation, start with
[Milestone 2 Research Summary](docs/milestone-2-research-summary.md).

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
uv run python scripts/run_turnover_stability_protocol.py
uv run python scripts/run_fresh_forward_monitoring.py
```

The baseline scripts write cached public data under `data/raw/` and a simple report under `artifacts/reports/`.
The feature script writes the monthly point-in-time feature table under `data/processed/`.
The evaluation scripts write diagnostic artifacts under `artifacts/reports/`.

## How To Read Results

- Treat reports as research diagnostics, not investment conclusions.
- Read [Milestone 2 Research Summary](docs/milestone-2-research-summary.md)
  before interpreting any performance table.
- The first locked validation run is a partial pass: it beats equal weight but
  does not clear the full benchmark panel.
- The turnover-stable branch reduces a known turnover failure mode, but it does
  not become fresh validation evidence.
- Fresh forward monitoring has no completed return yet; the first signal row is
  pending complete next-month data.
- Use [Docs Index](docs/index.md) for the full methodology trail.

## Milestone 1

Build the reproducible foundation:

- Download and cache ETF price data from Yahoo Finance via `yfinance`.
- Download and cache selected macro series from FRED/public sources.
- Write source manifests for downloaded data.
- Run a simple monthly rebalanced equal-weight ETF baseline.
- Generate a baseline markdown report with assumptions, metrics, and caveats.

Outperformance, model selection, and regime-aware allocation are deliberately deferred until milestone 2+.

## Milestone 2

Milestone 2 adds the first regime-aware research layer:

- monthly point-in-time macro/market feature table;
- conservative lag rules for public macro data;
- transparent four-state growth/inflation regime grid;
- walk-forward evaluation protocol before any strategy claims.

The current feature pipeline produces `data/processed/monthly_features.csv` and a matching manifest from cached raw data.
The current walk-forward pipeline produces a diagnostic report and aligned return/weight tables. It is a protocol check, not a robustness claim.

The milestone is now coherent as a GitHub portfolio artifact for research
process quality. The evidence remains diagnostic and should not be described as
a validated or investment-ready strategy.

## License

MIT License.
