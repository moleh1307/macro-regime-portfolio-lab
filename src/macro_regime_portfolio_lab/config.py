from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = PROJECT_ROOT / "configs"
DATA_DIR = PROJECT_ROOT / "data"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"


@dataclass(frozen=True)
class Asset:
    ticker: str
    name: str
    sleeve: str


def read_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        loaded = yaml.safe_load(file)
    if not isinstance(loaded, dict):
        raise ValueError(f"Expected YAML mapping in {path}")
    return loaded


def load_asset_universe(path: Path = CONFIG_DIR / "assets.yml") -> list[Asset]:
    config = read_yaml(path)
    universe = config.get("universe", [])
    if not isinstance(universe, list) or not universe:
        raise ValueError("Asset universe must be a non-empty list")
    return [Asset(**item) for item in universe]


def load_source_config(path: Path = CONFIG_DIR / "sources.yml") -> dict[str, Any]:
    return read_yaml(path)


def load_regime_feature_config(
    path: Path = CONFIG_DIR / "regime_features.yml",
) -> dict[str, Any]:
    return read_yaml(path)


def load_validation_config(path: Path = CONFIG_DIR / "validation.yml") -> dict[str, Any]:
    return read_yaml(path)
