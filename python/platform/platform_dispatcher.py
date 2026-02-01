from __future__ import annotations

import importlib
from typing import Any, Dict, TypedDict
import traceback

from shared.logger import logger
from shared.utils import DomainError
from config.config import get_platform
from python.platform.platform_contract import DispatchRequest
from python.platform.platform_contract import DispatchResult
from python.platform.platform_contract import NgResultStatus


def dispatch(request: DispatchRequest) -> DispatchResult:
    """
    Dispatch request to platform-specific command dispatcher.
    """

    if not isinstance(request, dict):
        raise DomainError("Invalid request")

    platform_name = get_platform()

    try:
        platform_dispatcher = _load_platform_dispatcher(platform_name)
    except Exception:
        return _build_error_result(
            f"Unsupported platform: {platform_name}",
            status="error",
        )

    try:
        return platform_dispatcher.dispatch(request)

    except Exception as exception:
        message = str(exception)
        logger.error("dispatch error:" + request.get("command", ""))
        logger.error(message)
        return _build_error_result(message, status="error")


def _load_platform_dispatcher(platform_name: str):
    module_path = f"platforms.{platform_name}.command_dispatcher"
    return importlib.import_module(module_path)


def _build_error_result(message: str, status: NgResultStatus) -> DispatchResult:
    return {
        "status": status,
        "message": message,
    }
