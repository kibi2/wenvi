import json
import sys
from typing import Any, Dict
from shared.logger import logger
from python.domain.utils import (
    focus_editable,
    set_editable_text,
    load_app_info,
    setStatus,
)
from python.platform.platform_dispatcher import dispatch
from python.domain.recovery_process import recovery_process
from global_ import GLOBAL
from python.platform.platform_contract import DispatchResult
from pathlib import Path


def write_form(text_file: str, save: str):
    try:
        logger.debug([text_file, save])
        try_write_form(text_file, save)
        setStatus(text_file, "close")
    except Exception as err:
        logger.error(getattr(err, "message", str(err)))
        setStatus(text_file, "close")
        recovery_process(text_file)


def is_save_mode(text_file: str, editable_info: Dict[str, Any], save: str) -> bool:
    if save == "off":
        return False
    if editable_info.get("status") == "close":
        return False
    if editable_info.get("status") == "error":
        return False
    assert editable_info.get("status") == "open", "invalid status"
    return True


def try_write_form(text_file: str, save: str):
    logger.debug(text_file)
    require_text_file_arg(text_file)

    editable_info = load_app_info(text_file)
    if not is_save_mode(text_file, editable_info, save):
        return
    GLOBAL["APP_NAME"] = editable_info["appName"]
    logger.debug(["===write_form:editable_info===", editable_info])

    result: DispatchResult = activate_browser_tab(editable_info["activeUrl"])
    assert "status" in result, "status must be present"
    if result["status"] != "ok":
        raise RuntimeError("no target of page")

    result = focus_editable(editable_info["editableId"])
    assert "status" in result, "status must be present"
    if result["status"] != "ok":
        raise RuntimeError("no target of editable")

    result = set_editable_text(text_file, editable_info["contentEditable"])
    assert "status" in result, "status must be present"
    logger.debug(json.dumps(result))
    if result["status"] != "ok":
        raise RuntimeError("cannot write text to editable")
    return


def require_text_file_arg(text_file: str):
    if not text_file:
        raise ValueError("TEXT_FILE not specified")


def activate_browser_tab(active_url: str) -> DispatchResult:
    return dispatch(
        {
            "command": "activate-browser-tab",
            "arguments": [active_url],
        }
    )


if __name__ == "__main__":
    write_form(sys.argv[1], sys.argv[2])
