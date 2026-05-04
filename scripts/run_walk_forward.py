from __future__ import annotations

import pandas as pd

from macro_regime_portfolio_lab.config import ARTIFACTS_DIR, DATA_DIR
from macro_regime_portfolio_lab.evaluation import (
    build_next_month_returns,
    run_regime_walk_forward,
)
from macro_regime_portfolio_lab.features import read_cached_prices
from macro_regime_portfolio_lab.reporting import write_walk_forward_report


def main() -> None:
    feature_path = DATA_DIR / "processed" / "monthly_features.csv"
    if not feature_path.exists():
        raise FileNotFoundError(
            f"Missing {feature_path}. Run `uv run python scripts/build_features.py` first."
        )

    prices = read_cached_prices()
    features = pd.read_csv(feature_path, index_col="date", parse_dates=True)
    next_returns = build_next_month_returns(prices)
    result = run_regime_walk_forward(features, next_returns)

    report_path = ARTIFACTS_DIR / "reports" / "walk_forward_diagnostic.md"
    returns_path = ARTIFACTS_DIR / "reports" / "walk_forward_returns.csv"
    weights_path = ARTIFACTS_DIR / "reports" / "walk_forward_weights.csv"

    write_walk_forward_report(result, report_path)
    result.returns.to_csv(returns_path)
    result.weights.to_csv(weights_path)

    print(f"report: {report_path}")
    print(f"returns: {returns_path}")
    print(f"weights: {weights_path}")
    for strategy_name, metrics in result.metrics.items():
        print(strategy_name)
        for metric_name, value in metrics.items():
            print(f"  {metric_name}: {value:.4f}")


if __name__ == "__main__":
    main()
