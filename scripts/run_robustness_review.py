from __future__ import annotations

import pandas as pd

from macro_regime_portfolio_lab.config import ARTIFACTS_DIR, DATA_DIR, PROJECT_ROOT
from macro_regime_portfolio_lab.evaluation import build_next_month_returns
from macro_regime_portfolio_lab.features import read_cached_prices
from macro_regime_portfolio_lab.robustness import RobustnessReview, run_robustness_review


def main() -> None:
    feature_path = DATA_DIR / "processed" / "monthly_features.csv"
    if not feature_path.exists():
        raise FileNotFoundError(
            f"Missing {feature_path}. Run `uv run python scripts/build_features.py` first."
        )

    prices = read_cached_prices()
    features = pd.read_csv(feature_path, index_col="date", parse_dates=True)
    next_returns = build_next_month_returns(prices)
    review = run_robustness_review(features, next_returns)

    report_dir = ARTIFACTS_DIR / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "full_sample": report_dir / "robustness_full_sample.csv",
        "subperiods": report_dir / "robustness_subperiods.csv",
        "stress_periods": report_dir / "robustness_stress_periods.csv",
        "rolling_windows": report_dir / "robustness_rolling_windows.csv",
        "buffer_subperiods": report_dir / "robustness_buffer_subperiods.csv",
        "bootstrap": report_dir / "robustness_bootstrap.csv",
    }

    review.full_sample.to_csv(paths["full_sample"], index=False)
    review.subperiods.to_csv(paths["subperiods"], index=False)
    review.stress_periods.to_csv(paths["stress_periods"], index=False)
    review.rolling_windows.to_csv(paths["rolling_windows"], index=False)
    review.buffer_subperiods.to_csv(paths["buffer_subperiods"], index=False)
    review.bootstrap.to_csv(paths["bootstrap"], index=False)

    doc_path = PROJECT_ROOT / "docs" / "robustness-review.md"
    doc_path.write_text(render_review_markdown(review), encoding="utf-8")

    print(f"review: {doc_path}")
    for name, path in paths.items():
        print(f"{name}: {path}")
    print("\nfull_sample")
    print(review.full_sample.round(4).to_string(index=False))
    print("\nbootstrap")
    print(review.bootstrap.round(4).to_string(index=False))


def render_review_markdown(review: RobustnessReview) -> str:
    full_sample = markdown_table(round_numeric(review.full_sample))
    stress = markdown_table(round_numeric(review.stress_periods))
    bootstrap = markdown_table(round_numeric(review.bootstrap))

    rolling = review.rolling_windows
    rolling_summary = pd.DataFrame.from_records(
        [
            {
                "check": "36m windows where strategy Sharpe > equal weight",
                "value": (
                    f"{int((rolling['strategy_minus_equal_weight_sharpe'] > 0).sum())} "
                    f"/ {len(rolling)}"
                ),
            },
            {
                "check": "36m windows where strategy Sharpe > static 60/40",
                "value": (
                    f"{int((rolling['strategy_minus_static_60_40_sharpe'] > 0).sum())} "
                    f"/ {len(rolling)}"
                ),
            },
            {
                "check": "median strategy minus equal-weight Sharpe",
                "value": round(float(rolling["strategy_minus_equal_weight_sharpe"].median()), 4),
            },
            {
                "check": "median strategy minus static-60/40 Sharpe",
                "value": round(float(rolling["strategy_minus_static_60_40_sharpe"].median()), 4),
            },
        ]
    )
    rolling_summary = markdown_table(rolling_summary)

    buffer_summary = (
        review.buffer_subperiods.groupby("switch_score_buffer")
        .agg(
            years_beating_equal_weight=(
                "strategy_minus_equal_weight",
                lambda values: int((values > 0).sum()),
            ),
            years_beating_static_60_40=(
                "strategy_minus_static_60_40",
                lambda values: int((values > 0).sum()),
            ),
            median_vs_equal_weight=("strategy_minus_equal_weight", "median"),
            median_turnover=("average_strategy_turnover", "median"),
        )
        .reset_index()
    )
    buffer_summary = round_numeric(buffer_summary)
    buffer_summary = markdown_table(buffer_summary)

    return f"""# Robustness Review

## Purpose

MRPL-016 adds a small robustness review for the post-MRPL-014 regime diagnostic.
This is still a diagnostic research artifact, not an outperformance claim,
investment recommendation, or tuned strategy selection.

## Inputs

- Default diagnostic setting: 0.10 switch-score buffer and 5 bps one-way turnover cost.
- Primary benchmark: monthly equal weight across the ETF universe.
- Additional benchmark: static SPY/TLT 60/40 target weights with the same turnover-cost convention.
- Evaluation rows: 215 signal months in the current walk-forward table.

## Full-Sample Metrics

{full_sample}

Interpretation: the regime diagnostic beats equal weight on full-sample net
Sharpe, but the static 60/40 benchmark is a harder comparator in this sample.

## Stress Periods

{stress}

Interpretation: the default diagnostic's strongest relative result is the
inflation/hiking-cycle period. The recent sample is weaker versus equal weight,
which reinforces that full-sample performance is not broad dominance.

## Rolling 36-Month Windows

{rolling_summary}

Interpretation: rolling windows show uneven evidence. A credible public claim
would need stability across windows, not only a favorable full-sample metric.

## Buffer Subperiod Check

{buffer_summary}

Interpretation: higher buffers remain promising, but the result still depends
on a turnover-control parameter. The 0.20 and 0.50 settings should not be
selected as defaults without a pre-declared validation rule.

## Block Bootstrap Sharpe Difference

{bootstrap}

Interpretation: the bootstrap is a coarse paired block diagnostic. It is useful
for uncertainty framing, but it is not a formal proof because monthly returns
are serially dependent and the allocation rule was developed on the same sample.

## Decision

The stricter regime diagnostic remains worth developing, but MRPL-016 does not
promote it to a robust outperformance claim. The next methodology step should
separate evaluation from research iteration more explicitly, either with a
pre-registered validation split, a stronger benchmark panel, or a walk-forward
model-selection protocol that prevents choosing parameters from the full grid.

## Output Tables

- `artifacts/reports/robustness_full_sample.csv`
- `artifacts/reports/robustness_subperiods.csv`
- `artifacts/reports/robustness_stress_periods.csv`
- `artifacts/reports/robustness_rolling_windows.csv`
- `artifacts/reports/robustness_buffer_subperiods.csv`
- `artifacts/reports/robustness_bootstrap.csv`
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
