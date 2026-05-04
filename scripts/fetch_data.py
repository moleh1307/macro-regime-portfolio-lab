from __future__ import annotations

from macro_regime_portfolio_lab.data import build_raw_data_cache


def main() -> None:
    outputs = build_raw_data_cache()
    for name, path in outputs.items():
        print(f"{name}: {path}")


if __name__ == "__main__":
    main()
