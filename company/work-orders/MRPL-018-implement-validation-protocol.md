# MRPL-018 - Implement Validation Protocol

- Owner role: Data Engineer / Quant Researcher
- Status: done
- Lifecycle state: Completed
- Risk lane: normal
- Canonical artifact: `docs/validation-results.md`

## Scope

Implement the MRPL-017 validation protocol in code and generate the first
validation result artifacts.

The implementation must preserve the locked validation boundary and avoid using
2022-forward data for parameter selection.

## Acceptance Criteria

- Add validation configuration for the fixed split and candidate grid.
- Add `scripts/run_validation_protocol.py` or equivalent reproducible CLI entry
  point.
- Select configurable parameters using only the research/calibration window.
- Evaluate the selected configuration once on the locked validation window.
- Compare against equal weight, static SPY/TLT 60/40, and SHY defensive proxy.
- Write machine-readable artifacts under `artifacts/reports/validation_*`.
- Write `docs/validation-results.md` with pass/fail language from
  `docs/validation-protocol.md`.
- Add tests for split boundaries and to verify selection excludes validation rows.

## Verification Evidence

- Added `configs/validation.yml`.
- Added `src/macro_regime_portfolio_lab/validation.py`.
- Added `scripts/run_validation_protocol.py`.
- Added `tests/test_validation.py`.
- Generated `docs/validation-results.md`.
- Generated validation artifacts under `artifacts/reports/validation_*`.
- Selection used only 2008-05-31 through 2021-12-31 research rows.
- Selected configuration: switch-score buffer 0.50, min regime history 12, top_n 4, fallback SHY, 5 bps cost.
- Locked validation window: 2022-01-31 through 2026-03-31, 51 rows.
- Locked validation metrics: regime diagnostic net Sharpe 1.0911; equal-weight net Sharpe 0.8266; static 60/40 net Sharpe 0.3194; SHY net Sharpe 1.1053.
- Interpretation: beats equal weight only; does not clear the full benchmark panel because SHY has slightly higher validation Sharpe and much lower drawdown.
- `uv run pytest` passed: 25 tests.
- `uv run ruff check .` passed.
- `uv run python scripts/run_validation_protocol.py` generated the validation report and tables.

## Blocker / Decision Needed

- None.

## Closeout State

- Completed. Next work should review validation results and decide the next methodology direction without strengthening performance claims.
