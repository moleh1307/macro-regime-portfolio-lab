from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from macro_regime_portfolio_lab.config import (
    ARTIFACTS_DIR,
    DATA_DIR,
    PROJECT_ROOT,
    load_fresh_forward_monitoring_config,
)
from macro_regime_portfolio_lab.evaluation import build_next_month_returns
from macro_regime_portfolio_lab.features import read_cached_prices
from macro_regime_portfolio_lab.fresh_forward import (
    FreshForwardMonitoringResult,
    parse_fresh_forward_monitoring_config,
    run_fresh_forward_monitoring,
)


def main() -> None:
    feature_path = DATA_DIR / "processed" / "monthly_features.csv"
    if not feature_path.exists():
        raise FileNotFoundError(
            f"Missing {feature_path}. Run `uv run python scripts/build_features.py` first."
        )

    config = parse_fresh_forward_monitoring_config(
        load_fresh_forward_monitoring_config()
    )
    prices = read_cached_prices()
    features = pd.read_csv(feature_path, index_col="date", parse_dates=True)
    next_returns = build_next_month_returns(prices)
    result = run_fresh_forward_monitoring(features, next_returns, config)

    report_dir = ARTIFACTS_DIR / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "returns": report_dir / "fresh_forward_monitoring_returns.csv",
        "metrics": report_dir / "fresh_forward_monitoring_metrics.csv",
        "warnings": report_dir / "fresh_forward_monitoring_warnings.csv",
        "pending_signals": report_dir / "fresh_forward_monitoring_pending_signals.csv",
    }
    result.completed_returns.to_csv(paths["returns"])
    result.metrics.to_csv(paths["metrics"], index=False)
    result.warnings.to_csv(paths["warnings"], index=False)
    result.pending_signals.to_csv(paths["pending_signals"], index=False)

    doc_path = PROJECT_ROOT / "docs" / "fresh-data-forward-monitoring.md"
    doc_path.write_text(
        render_monitoring_markdown(
            result=result,
            source_boundaries=read_source_boundaries(),
        ),
        encoding="utf-8",
    )

    print(f"fresh_forward_monitoring: {doc_path}")
    for name, path in paths.items():
        print(f"{name}: {path}")
    print("\nboundary")
    print(format_boundary_for_console(result.boundary))
    print("\nmetrics")
    print(result.metrics.to_string(index=False))


def read_source_boundaries() -> dict[str, str]:
    manifests = {
        "yfinance_adjusted_prices": DATA_DIR / "raw" / "yfinance" / "manifest.json",
        "fred_macro_cache": DATA_DIR / "raw" / "fred" / "manifest.json",
        "monthly_features": DATA_DIR / "processed" / "monthly_features_manifest.json",
    }
    boundaries = {}
    for name, path in manifests.items():
        boundaries[name] = read_manifest_end(path)
    return boundaries


def read_manifest_end(path: Path) -> str:
    if not path.exists():
        return "missing_manifest"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    return str(manifest.get("end", "missing_end"))


def render_monitoring_markdown(
    *,
    result: FreshForwardMonitoringResult,
    source_boundaries: dict[str, str],
) -> str:
    boundary = pd.DataFrame.from_records([result.boundary])
    frozen_rule = pd.DataFrame.from_records([result.frozen_rule])
    source_frame = pd.DataFrame(
        [{"source": source, "current_end": end} for source, end in source_boundaries.items()]
    )
    completed_count = int(result.boundary["completed_monitoring_rows"])
    pending_count = int(result.boundary["pending_signal_rows"])
    status_text = monitoring_status_text(
        completed_count=completed_count,
        pending_count=pending_count,
    )

    return f"""# Fresh-Data-Forward Monitoring

## Purpose

MRPL-024 implements the report scaffold from
`docs/fresh-data-forward-monitoring-protocol.md`.

This is a monitoring scaffold for future completed monthly observations. It is
not a fresh validation result, live trading signal, or outperformance claim.

## Current Status

{status_text}

## Source Boundaries

{markdown_table(source_frame)}

## Monitoring Boundary

{markdown_table(round_numeric(boundary))}

## Frozen Rule

{markdown_table(round_numeric(frozen_rule))}

## Completed Monitoring Returns

{markdown_table(round_numeric(result.completed_returns.reset_index()))}

## Pending Signals

{markdown_table(round_numeric(result.pending_signals))}

## Monitoring Metrics

{markdown_table(round_numeric(result.metrics))}

## Warnings

{markdown_table(round_numeric(result.warnings))}

## Claim Boundary

Allowed language:

- "The monitoring scaffold is ready for future completed monthly observations."
- "The 2026-04-30 signal row is pending a complete next-month return."
- "Monitoring evidence remains diagnostic until enough genuinely new rows
  accumulate."

Not allowed:

- robust outperformance;
- fresh validation;
- live trading signal;
- investment-ready allocation;
- alpha claim.

## Output Tables

- `artifacts/reports/fresh_forward_monitoring_returns.csv`
- `artifacts/reports/fresh_forward_monitoring_metrics.csv`
- `artifacts/reports/fresh_forward_monitoring_warnings.csv`
- `artifacts/reports/fresh_forward_monitoring_pending_signals.csv`
"""


def monitoring_status_text(*, completed_count: int, pending_count: int) -> str:
    if completed_count == 0 and pending_count > 0:
        return (
            "No completed forward-monitoring return exists in the current cached data. "
            "The first monitoring signal is recorded as pending and must wait for a "
            "complete next-month price observation."
        )
    if completed_count == 0:
        return "No completed or pending forward-monitoring rows are available."
    return f"Completed forward-monitoring rows: {completed_count}."


def markdown_table(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "_No rows._"
    columns = list(frame.columns)
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    rows = [
        "| " + " | ".join(format_markdown_value(row[column]) for column in columns) + " |"
        for _, row in frame.iterrows()
    ]
    return "\n".join([header, separator, *rows])


def round_numeric(frame: pd.DataFrame, decimals: int = 4) -> pd.DataFrame:
    rounded = frame.copy()
    numeric_columns = rounded.select_dtypes(include="number").columns
    rounded.loc[:, numeric_columns] = rounded.loc[:, numeric_columns].round(decimals)
    return rounded


def format_markdown_value(value: object) -> str:
    if pd.isna(value):
        return ""
    if isinstance(value, float):
        return f"{value:.4f}"
    if isinstance(value, pd.Timestamp):
        return value.strftime("%Y-%m-%d")
    return str(value)


def format_boundary_for_console(
    boundary: dict[str, pd.Timestamp | int | str | None],
) -> dict[str, str | int | None]:
    formatted = {}
    for key, value in boundary.items():
        if isinstance(value, pd.Timestamp):
            formatted[key] = value.strftime("%Y-%m-%d")
        else:
            formatted[key] = value
    return formatted


if __name__ == "__main__":
    main()
