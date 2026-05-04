from __future__ import annotations

import pandas as pd

from macro_regime_portfolio_lab.config import ARTIFACTS_DIR, DATA_DIR
from macro_regime_portfolio_lab.evaluation import (
    build_next_month_returns,
    run_parameter_sensitivity_grid,
)
from macro_regime_portfolio_lab.features import read_cached_prices


def main() -> None:
    feature_path = DATA_DIR / "processed" / "monthly_features.csv"
    if not feature_path.exists():
        raise FileNotFoundError(
            f"Missing {feature_path}. Run `uv run python scripts/build_features.py` first."
        )

    prices = read_cached_prices()
    features = pd.read_csv(feature_path, index_col="date", parse_dates=True)
    next_returns = build_next_month_returns(prices)
    grid = run_parameter_sensitivity_grid(
        features,
        next_returns,
        switch_score_buffers=[0.0, 0.05, 0.10, 0.20, 0.50],
        cost_bps_values=[0.0, 5.0, 10.0, 25.0],
    )

    output_path = ARTIFACTS_DIR / "reports" / "parameter_sensitivity.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    grid.to_csv(output_path, index=False)

    print(f"sensitivity: {output_path}")
    print(grid.sort_values("strategy_net_sharpe", ascending=False).to_string(index=False))


if __name__ == "__main__":
    main()
