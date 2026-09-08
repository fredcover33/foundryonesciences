"""Configuration loading.

Every key required by the picker must be present in config.toml. There are no
defaults in code: a missing key is fatal.
"""

from __future__ import annotations

import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# Dotted paths of every key config.toml must define. No key has a default.
REQUIRED_KEYS: tuple[str, ...] = (
    "probe.trades_file_size_guard_gb",
    "probe.trades_stream_sample_seconds",
    "probe.target_replay_sessions",
    "paths.download_dir",
    "paths.store_path",
)


class ConfigMissingKey(Exception):
    """Raised when config.toml does not define a required key."""

    def __init__(self, key: str) -> None:
        self.key = key
        super().__init__(f"CONFIG MISSING: {key}")


@dataclass(frozen=True)
class Config:
    trades_file_size_guard_gb: float
    trades_stream_sample_seconds: int
    target_replay_sessions: int
    download_dir: str
    store_path: str


def _lookup(data: dict[str, Any], dotted: str) -> Any:
    node: Any = data
    for part in dotted.split("."):
        if not isinstance(node, dict) or part not in node:
            raise ConfigMissingKey(dotted)
        node = node[part]
    return node


def load_config_data(data: dict[str, Any]) -> Config:
    """Build a Config from an already-parsed TOML mapping.

    Raises ConfigMissingKey for the first missing required key.
    """
    for key in REQUIRED_KEYS:
        _lookup(data, key)
    return Config(
        trades_file_size_guard_gb=float(_lookup(data, "probe.trades_file_size_guard_gb")),
        trades_stream_sample_seconds=int(_lookup(data, "probe.trades_stream_sample_seconds")),
        target_replay_sessions=int(_lookup(data, "probe.target_replay_sessions")),
        download_dir=str(_lookup(data, "paths.download_dir")),
        store_path=str(_lookup(data, "paths.store_path")),
    )


def load_config(path: str | Path = "config.toml") -> Config:
    with open(path, "rb") as fh:
        return load_config_data(tomllib.load(fh))


def main(argv: list[str] | None = None) -> int:
    """CLI entry point: load config, or exit with CONFIG MISSING: <key>."""
    argv = list(sys.argv[1:] if argv is None else argv)
    path = argv[0] if argv else "config.toml"
    try:
        load_config(path)
    except ConfigMissingKey as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
