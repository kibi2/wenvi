from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Optional, Any, Dict

from config.load_toml import load_toml_config
from config.types import UserConfig

_cached_config: Optional[UserConfig] = None


def get_config() -> UserConfig:
    global _cached_config
    if _cached_config is None:
        data = load_toml_config()  # type: Dict[str, Any]
        _cached_config = UserConfig.from_dict(data)
    return _cached_config


Platform = str


def _normalize_platform(p: Any) -> Platform:
    v = str(p).lower()
    if v in ("darwin", "mac", "macos"):
        return "macos"
    if v in ("win32", "win", "windows"):
        return "windows"
    if v == "linux":
        return "linux"
    return v


def get_platform() -> Platform:
    env_platform = os.environ.get("WENVI_PLATFORM")
    if env_platform:
        return _normalize_platform(env_platform)

    config = get_config()
    if getattr(config, "platform", None):
        return _normalize_platform(config.platform)

    return _normalize_platform(sys.platform)


def _expand_home(p: str) -> Path:
    if p.startswith("~"):
        return Path(p).expanduser()
    return Path(p)


def get_data_home() -> Path:
    config = get_config()
    if config.dataHome is not None:
        return _expand_home(config.dataHome)

    platform = get_platform()
    home = Path.home()

    if platform in ("macos", "linux"):
        return home / ".cache" / "wenvi"

    if platform == "windows":
        local_appdata = os.environ.get("LOCALAPPDATA")
        base = Path(local_appdata) if local_appdata else home
        return base / "wenvi"

    return home / ".cache" / "wenvi"
