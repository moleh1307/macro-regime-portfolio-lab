from __future__ import annotations

from macro_regime_portfolio_lab.features import build_processed_feature_cache


def main() -> None:
    outputs = build_processed_feature_cache()
    for name, path in outputs.items():
        print(f"{name}: {path}")


if __name__ == "__main__":
    main()
