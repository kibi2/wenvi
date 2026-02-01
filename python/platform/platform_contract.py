from __future__ import annotations
from typing import TypedDict, List, Optional, Literal, Literal, Union


NgResultStatus = Literal["error", "warn", "ok"]


class DispatchRequest(TypedDict, total=False):
    command: str
    arguments: Optional[List[str]]


class DispatchResult(TypedDict, total=False):
    status: NgResultStatus
    message: str
    result: str
    bundleId: str
    appName: str
    activeUrl: str
    title: str
    hostName: str
    editableId: str
    editableText: str
    contentEditable: str
