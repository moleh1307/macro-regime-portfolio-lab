# MRPL-012 - Run Parameter Sensitivity Grid

- Owner role: Quant Researcher / Research Engineer
- Status: done
- Lifecycle state: Done
- Risk lane: normal
- Canonical artifact: `artifacts/reports/parameter_sensitivity.csv`

## Scope

Run a small diagnostic sensitivity grid before accepting any allocation rule as the milestone default:

- vary switch-score buffer values;
- vary transaction-cost assumptions;
- compare net Sharpe, net return, max drawdown, and turnover;
- keep conclusions diagnostic only.

## Acceptance Criteria

- Add a reproducible sensitivity script or function.
- Generate a compact CSV/table artifact.
- Document which settings look fragile versus stable.
- Do not tune the default purely to maximize historical performance.

## Verification Evidence

- Added `run_parameter_sensitivity_grid` to `src/macro_regime_portfolio_lab/evaluation.py`.
- Added `scripts/run_parameter_sensitivity.py`.
- Added `docs/parameter-sensitivity.md`.
- Added test coverage for grid shape and required output columns.
- `uv run pytest`: 18 passed.
- `uv run ruff check .`: all checks passed.
- `uv run python scripts/run_parameter_sensitivity.py` completed.
- Generated `artifacts/reports/parameter_sensitivity.csv` with 20 rows.
- Finding: every tested regime-diagnostic setting had lower net Sharpe than equal weight.
- Best regime-diagnostic net Sharpe was 0.6633 at buffer 0.00 and 0 bps cost; equal-weight net Sharpe at 0 bps was 0.6903.

## Blocker / Decision Needed

- None.

## Closeout State

- Done.
