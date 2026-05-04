from macro_regime_portfolio_lab.config import load_asset_universe, load_source_config


def test_default_asset_universe_matches_v0_scope() -> None:
    assets = load_asset_universe()
    tickers = [asset.ticker for asset in assets]

    assert tickers == [
        "SPY",
        "QQQ",
        "IWM",
        "EFA",
        "EEM",
        "TLT",
        "IEF",
        "GLD",
        "DBC",
        "VNQ",
        "UUP",
        "SHY",
    ]


def test_source_config_uses_public_no_key_defaults() -> None:
    sources = load_source_config()

    assert sources["prices"]["provider"] == "yfinance"
    assert sources["macro"]["provider"] == "fred"
    assert "api_key" not in sources["macro"]
