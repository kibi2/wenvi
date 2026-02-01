from __future__ import annotations

import importlib
from typing import Any, Dict, List, Protocol, TypedDict
import traceback

from shared.logger import logger
from shared.utils import DomainError


class DispatchRequest(TypedDict):
    command: str
    arguments: List[str]


class DispatchResult(TypedDict, total=False):
    status: str
    result: Any
    message: str


class HandlerModule(Protocol):
    def entry(self, args: List[str]) -> DispatchResult: ...


def dispatch(request: DispatchRequest) -> DispatchResult:
    command = request.get("command")
    args = request.get("arguments") or []

    try:
        handler = _load_handler_module(command)
        return _invoke_handler(handler, args)

    except DomainError as error:
        message = str(error)
        logger.error("mac dispatch DomainError:" + command)
        logger.error(error)
        logger.error(traceback.format_exc())
        return _build_error_result(message, error.status)

    except Exception as error:
        logger.error("mac dispatch exception:" + command)
        logger.error(error)
        logger.error(traceback.format_exc())
        return _build_error_result(str(error), "error")


def _load_handler_module(command: str) -> HandlerModule:
    module_path = f"platforms.macos.handlers.{command}"

    try:
        module = importlib.import_module(module_path)
    except ModuleNotFoundError as exc:
        raise DomainError(f'Handler "{command}" not found') from exc

    if not _is_valid_handler_module(module):
        raise DomainError(f'Handler "{command}" does not export entry()')

    return module  # type: ignore[return-value]


def _is_valid_handler_module(module: object) -> bool:
    return hasattr(module, "entry") and callable(getattr(module, "entry"))


def _invoke_handler(
    handler: HandlerModule,
    args: List[str],
) -> DispatchResult:
    return handler.entry(args)


def _build_error_result(message: str, status: str) -> DispatchResult:
    return {
        "status": status,
        "message": message,
    }
