from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

import pandas as pd
import yfinance as yf

from macro_regime_portfolio_lab.config import DATA_DIR, load_asset_universe, load_source_config


def fetch_adjusted_prices(start: str | None = None) -> pd.DataFrame:
    assets = load_asset_universe()
    source_config = load_source_config()
    tickers = [asset.ticker for asset in assets]
    start_date = start or source_config["prices"]["start"]

    raw = yf.download(
        tickers=tickers,
        start=start_date,
        auto_adjust=True,
        progress=False,
        group_by="column",
    )
    if raw.empty:
        raise RuntimeError("No price data returned by yfinance")

    if isinstance(raw.columns, pd.MultiIndex):
        prices = raw["Close"]
    else:
        prices = raw[["Close"]].rename(columns={"Close": tickers[0]})

    prices = prices.sort_index().dropna(how="all")
    prices.index.name = "date"
    return prices


def fetch_fred_series(start: str | None = None) -> pd.DataFrame:
    source_config = load_source_config()
    start_date = start or source_config["macro"]["start"]
    series = source_config["macro"]["series"]

    frames = []
    for item in series:
        query = urlencode({"id": item["id"]})
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?{query}"
        frame = pd.read_csv(url, parse_dates=["observation_date"], na_values=["."])
        frame = frame.rename(
            columns={
                "observation_date": "date",
                item["id"]: item["name"],
            }
        )
        frame = frame.set_index("date")
        frame = frame.loc[frame.index >= pd.Timestamp(start_date)]
        frames.append(frame)

    macro = pd.concat(frames, axis=1).sort_index()
    macro.index.name = "date"
    return macro


def write_dataset_with_manifest(
    frame: pd.DataFrame,
    dataset_path: Path,
    manifest_path: Path,
    source: dict[str, Any],
) -> None:
    dataset_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    frame.to_csv(dataset_path)
    manifest = {
        "created_at_utc": datetime.now(UTC).isoformat(),
        "dataset_path": str(dataset_path),
        "rows": int(len(frame)),
        "columns": list(frame.columns),
        "start": str(frame.index.min().date()) if len(frame) else None,
        "end": str(frame.index.max().date()) if len(frame) else None,
        "source": source,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def build_raw_data_cache() -> dict[str, Path]:
    source_config = load_source_config()
    price_data = fetch_adjusted_prices()
    macro_data = fetch_fred_series()

    price_path = DATA_DIR / "raw" / "yfinance" / "adjusted_prices.csv"
    price_manifest_path = DATA_DIR / "raw" / "yfinance" / "manifest.json"
    macro_path = DATA_DIR / "raw" / "fred" / "macro_series.csv"
    macro_manifest_path = DATA_DIR / "raw" / "fred" / "manifest.json"

    write_dataset_with_manifest(
        price_data,
        price_path,
        price_manifest_path,
        {"provider": "yfinance", "config": source_config["prices"]},
    )
    write_dataset_with_manifest(
        macro_data,
        macro_path,
        macro_manifest_path,
        {"provider": "fred", "config": source_config["macro"]},
    )

    return {
        "prices": price_path,
        "prices_manifest": price_manifest_path,
        "macro": macro_path,
        "macro_manifest": macro_manifest_path,
    }
