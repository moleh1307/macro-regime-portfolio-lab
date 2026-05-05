from __future__ import annotations

import pandas as pd

from macro_regime_portfolio_lab.config import (
    ARTIFACTS_DIR,
    DATA_DIR,
    PROJECT_ROOT,
    load_turnover_stability_config,
)
from macro_regime_portfolio_lab.evaluation import build_next_month_returns
from macro_regime_portfolio_lab.features import read_cached_prices
from macro_regime_portfolio_lab.turnover_stability import (
    POST_HOLDOUT_REVIEW_LABEL,
    TurnoverStabilityResult,
    parse_turnover_stability_config,
    run_turnover_stability_protocol,
)


def main() -> None:
    feature_path = DATA_DIR / "processed" / "monthly_features.csv"
    if not feature_path.exists():
        raise FileNotFoundError(
            f"Missing {feature_path}. Run `uv run python scripts/build_features.py` first."
        )

    config = parse_turnover_stability_config(load_turnover_stability_config())
    prices = read_cached_prices()
    features = pd.read_csv(feature_path, index_col="date", parse_dates=True)
    next_returns = build_next_month_returns(prices)
    result = run_turnover_stability_protocol(features, next_returns, config)

    report_dir = ARTIFACTS_DIR / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "candidate_grid": report_dir / "turnover_stability_candidate_grid.csv",
        "post_holdout_returns": report_dir / "turnover_stability_post_holdout_returns.csv",
        "post_holdout_metrics": report_dir / "turnover_stability_post_holdout_metrics.csv",
        "calendar_years": report_dir / "turnover_stability_calendar_years.csv",
        "stress_periods": report_dir / "turnover_stability_stress_periods.csv",
        "bootstrap": report_dir / "turnover_stability_bootstrap.csv",
    }
    result.candidate_grid.to_csv(paths["candidate_grid"], index=False)
    result.post_holdout_returns.to_csv(paths["post_holdout_returns"])
    result.post_holdout_metrics.to_csv(paths["post_holdout_metrics"], index=False)
    result.post_holdout_calendar_years.to_csv(paths["calendar_years"], index=False)
    result.post_holdout_stress_periods.to_csv(paths["stress_periods"], index=False)
    result.post_holdout_bootstrap.to_csv(paths["bootstrap"], index=False)

    doc_path = PROJECT_ROOT / "docs" / "turnover-stability-results.md"
    doc_path.write_text(render_results_markdown(result), encoding="utf-8")

    print(f"turnover_stability_results: {doc_path}")
    for name, path in paths.items():
        print(f"{name}: {path}")
    print("\nselected_config")
    print(result.selected_config)
    print("\npost_holdout_metrics")
    print(result.post_holdout_metrics.round(4).to_string(index=False))
    print(f"\ninterpretation: {result.interpretation}")


def render_results_markdown(result: TurnoverStabilityResult) -> str:
    selected = pd.DataFrame.from_records([result.selected_config])
    top_candidates = result.candidate_grid.head(10)
    rejected_count = int((~result.candidate_grid["passes_turnover_stability"]).sum())
    passed_count = int(result.candidate_grid["passes_turnover_stability"].sum())
    interpretation_text = {
        "turnover_stability_reduced_known_failure_mode": (
            "The turnover-stability protocol reduced the known turnover failure mode. "
            "Because the 2022-forward period had already been inspected, this remains "
            "a post-holdout-review diagnostic, not fresh independent validation."
        ),
        "partial_post_holdout_review_diagnostic": (
            "The second-cycle diagnostic remains partial and requires future fresh data. "
            "It keeps the result in research-scaffold territory."
        ),
        "failed_defensive_benchmark_hurdle": (
            "The second-cycle protocol did not clear the defensive benchmark hurdle. "
            "The result remains diagnostic and should not be used for performance claims."
        ),
        "second_cycle_diagnostic_inconclusive": (
            "The second-cycle diagnostic is inconclusive and should be treated as method "
            "development evidence only."
        ),
    }[result.interpretation]

    return f"""# Turnover Stability Results

## Purpose

MRPL-021 implements `docs/turnover-stability-protocol.md`.

Report label:

```text
{POST_HOLDOUT_REVIEW_LABEL}
```

The 2022-forward period has already been inspected in MRPL-018. This run tests
whether a research-window turnover-stability protocol addresses a known failure
mode, but it is not a fresh independent holdout.

The turnover-stability metrics exclude the configured initial deployment warmup
months from the research-window turnover screen. This prevents the first
portfolio deployment from being treated as recurring allocation instability.

## Selected Configuration

{markdown_table(round_numeric(selected))}

## Candidate Screen

- candidates passing hard turnover-stability thresholds: {passed_count}
- candidates rejected before ranking: {rejected_count}

Top candidate rows:

{markdown_table(round_numeric(top_candidates))}

## Post-Holdout-Review Metrics

{markdown_table(round_numeric(result.post_holdout_metrics))}

## Calendar-Year Returns

{markdown_table(round_numeric(result.post_holdout_calendar_years))}

## Stress Periods

{markdown_table(round_numeric(result.post_holdout_stress_periods))}

## Bootstrap Sharpe Differences

{markdown_table(round_numeric(result.post_holdout_bootstrap))}

## Interpretation

{interpretation_text}

Do not describe this as robust outperformance, final validation, fresh holdout
evidence, or an investment-ready strategy.

## Output Tables

- `artifacts/reports/turnover_stability_candidate_grid.csv`
- `artifacts/reports/turnover_stability_post_holdout_returns.csv`
- `artifacts/reports/turnover_stability_post_holdout_metrics.csv`
- `artifacts/reports/turnover_stability_calendar_years.csv`
- `artifacts/reports/turnover_stability_stress_periods.csv`
- `artifacts/reports/turnover_stability_bootstrap.csv`
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
