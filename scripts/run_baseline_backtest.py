from __future__ import annotations

import pandas as pd

from macro_regime_portfolio_lab.backtest import monthly_equal_weight_returns
from macro_regime_portfolio_lab.config import ARTIFACTS_DIR, DATA_DIR
from macro_regime_portfolio_lab.reporting import write_baseline_report


def main() -> None:
    price_path = DATA_DIR / "raw" / "yfinance" / "adjusted_prices.csv"
    if not price_path.exists():
        raise FileNotFoundError(
            f"Missing {price_path}. Run `uv run python scripts/fetch_data.py` first."
        )

    prices = pd.read_csv(price_path, index_col="date", parse_dates=True)
    result = monthly_equal_weight_returns(prices)

    report_path = ARTIFACTS_DIR / "reports" / "baseline_equal_weight.md"
    write_baseline_report(result, report_path)
    print(f"report: {report_path}")
    for name, value in result.metrics.items():
        print(f"{name}: {value:.4f}")


if __name__ == "__main__":
    main()
