from typing import Final, TypedDict


class GlobalConfig(TypedDict):
    APP_NAME: str


GLOBAL: Final[GlobalConfig] = {
    "APP_NAME": "Google Chrome",
}
