from __future__ import annotations

from typing import Any, Dict, List

from python.platform.platform_contract import DispatchResult
from platforms.macos.invoke_osa import invoke_osa
from shared.utils import assert_
from shared.logger import logger


def entry(arguments_object: List[str]) -> DispatchResult:
    assert_(
        isinstance(arguments_object, list) and len(arguments_object) in (1, 2),
        "need message [option] for dialog",
    )

    try:
        _show_dialog(arguments_object)
        return {
            "status": "ok",
            "result": "ok",
        }

    except Exception as exception:
        logger.debug(str(exception))
        # Dialog cancel is treated as normal outcome
        return {
            "status": "ok",
            "result": "cancel",
        }


def _show_dialog(arguments_object: List[str]) -> None:
    invoke_osa("display-dialog", arguments_object)
