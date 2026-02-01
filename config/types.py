from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class UserConfig:
    platform: Optional[str] = None
    dataHome: Optional[str] = None
    editor: Optional[str] = None

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "UserConfig":
        """
        Create UserConfig from dict (e.g. parsed TOML).
        Unknown keys are ignored.
        """
        return UserConfig(
            platform=data.get("platform"),
            dataHome=data.get("dataHome"),
            editor=data.get("editor"),
        )
