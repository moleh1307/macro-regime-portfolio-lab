from __future__ import annotations

import pandas as pd

from macro_regime_portfolio_lab.config import (
    ARTIFACTS_DIR,
    DATA_DIR,
    PROJECT_ROOT,
    load_validation_config,
)
from macro_regime_portfolio_lab.evaluation import build_next_month_returns
from macro_regime_portfolio_lab.features import read_cached_prices
from macro_regime_portfolio_lab.validation import (
    ValidationResult,
    parse_validation_config,
    run_validation_protocol,
)


def main() -> None:
    feature_path = DATA_DIR / "processed" / "monthly_features.csv"
    if not feature_path.exists():
        raise FileNotFoundError(
            f"Missing {feature_path}. Run `uv run python scripts/build_features.py` first."
        )

    validation_config = parse_validation_config(load_validation_config())
    prices = read_cached_prices()
    features = pd.read_csv(feature_path, index_col="date", parse_dates=True)
    next_returns = build_next_month_returns(prices)
    result = run_validation_protocol(features, next_returns, validation_config)

    report_dir = ARTIFACTS_DIR / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "selection_grid": report_dir / "validation_selection_grid.csv",
        "returns": report_dir / "validation_returns.csv",
        "metrics": report_dir / "validation_metrics.csv",
        "calendar_years": report_dir / "validation_calendar_years.csv",
        "stress_periods": report_dir / "validation_stress_periods.csv",
        "bootstrap": report_dir / "validation_bootstrap.csv",
    }

    result.selection_grid.to_csv(paths["selection_grid"], index=False)
    result.validation_returns.to_csv(paths["returns"])
    result.validation_metrics.to_csv(paths["metrics"], index=False)
    result.validation_calendar_years.to_csv(paths["calendar_years"], index=False)
    result.validation_stress_periods.to_csv(paths["stress_periods"], index=False)
    result.validation_bootstrap.to_csv(paths["bootstrap"], index=False)

    doc_path = PROJECT_ROOT / "docs" / "validation-results.md"
    doc_path.write_text(render_validation_markdown(result), encoding="utf-8")

    print(f"validation_results: {doc_path}")
    for name, path in paths.items():
        print(f"{name}: {path}")
    print("\nselected_config")
    print(result.selected_config)
    print("\nvalidation_metrics")
    print(result.validation_metrics.round(4).to_string(index=False))
    print(f"\ninterpretation: {result.interpretation}")


def render_validation_markdown(result: ValidationResult) -> str:
    selected = pd.DataFrame.from_records([result.selected_config])
    selection_top = result.selection_grid.head(10)
    metrics = result.validation_metrics
    calendar_years = result.validation_calendar_years
    stress = result.validation_stress_periods
    bootstrap = result.validation_bootstrap

    interpretation_text = {
        "passed_benchmark_panel": (
            "The strategy passed the first validation screen against the benchmark panel. "
            "This supports continued research into the transparent regime-aware allocation "
            "scaffold, but does not convert the project into an investment strategy."
        ),
        "beats_equal_weight_only": (
            "The diagnostic improves on equal weight in the locked validation window but "
            "does not clear the full benchmark panel. The result remains research-scaffold "
            "evidence, not an outperformance claim."
        ),
        "rejected_current_diagnostic": (
            "The validation protocol rejected the current diagnostic allocation. The repo "
            "preserves the pipeline and negative result as part of reproducible research."
        ),
    }[result.interpretation]

    return f"""# Validation Results

## Purpose

MRPL-018 implements the locked validation protocol from
`docs/validation-protocol.md`.

This report is a diagnostic validation artifact. It is not an investment
recommendation, production strategy, or robust outperformance claim.

## Selected Configuration

{markdown_table(round_numeric(selected))}

Selection used only the research/calibration window ending on 2021-12-31. The
locked validation rows starting in 2022 were not available to the parameter
selection step.

## Selection Grid Top Rows

{markdown_table(round_numeric(selection_top))}

The selection objective is the median rolling 36-month Sharpe difference versus
the strongest benchmark in each window, subject to average monthly turnover at
or below 0.12.

## Locked Validation Metrics

{markdown_table(round_numeric(metrics))}

## Calendar-Year Validation Returns

{markdown_table(round_numeric(calendar_years))}

## Validation Stress Periods

{markdown_table(round_numeric(stress))}

## Block Bootstrap Sharpe Differences

{markdown_table(round_numeric(bootstrap))}

The bootstrap is a coarse paired block diagnostic. It frames uncertainty around
Sharpe differences, but it does not prove robustness.

## Interpretation

{interpretation_text}

## Output Tables

- `artifacts/reports/validation_selection_grid.csv`
- `artifacts/reports/validation_returns.csv`
- `artifacts/reports/validation_metrics.csv`
- `artifacts/reports/validation_calendar_years.csv`
- `artifacts/reports/validation_stress_periods.csv`
- `artifacts/reports/validation_bootstrap.csv`
"""


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


if __name__ == "__main__":
    main()
