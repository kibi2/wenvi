from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

try:
    import toml  # pip install toml
except ImportError as e:
    toml = None


CONFIG_PATH = Path.home() / ".config" / "wenvi" / "config.toml"


def load_toml_config() -> Dict[str, Any]:
    if not CONFIG_PATH.exists():
        return {}
    if toml is None:
        return {}

    try:
        text = CONFIG_PATH.read_text(encoding="utf-8")
        data = toml.loads(text)

        if isinstance(data, dict):
            return data

        return {}
    except Exception as err:
        print("[wenvi] failed to load config.toml:", err)
        return {}
