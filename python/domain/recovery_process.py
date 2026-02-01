from shared.logger import logger
from pathlib import Path
from global_ import GLOBAL
from python.platform.platform_dispatcher import dispatch
from python.platform.platform_contract import DispatchResult
from python.platform.platform_contract import DispatchRequest
from python.domain.utils import (
    display_dialog,
    make_symbolic_file,
    focus_editable,
    set_editable_text,
    load_app_info,
    setStatus,
)


def recovery_process(text_file: str):
    if not confirm_recover(text_file):
        return

    editable_info = load_app_info(text_file)
    GLOBAL["APP_NAME"] = editable_info["appName"]

    if re_write_text_to_editable(editable_info, text_file):
        return

    setStatus(text_file, "error")
    last_resort(text_file)


def confirm_recover(text_file) -> bool:
    last_json = str(Path(text_file).parent) + "/last.json"
    last_text = str(Path(text_file).parent) + "/last.txt"
    result = display_dialog(
        f"""
The original page cannot be found.
Do you want to open the page and export it?

Your edits have not been lost.
Please check the files below.

{last_json}

{last_text}
        """
    )
    logger.debug("[confirm] result= ", result)
    assert "result" in result, "result must be present"
    return result["result"] == "ok"


def re_open_browser_with_url(editable_info: dict) -> DispatchResult:
    payload: DispatchRequest = {
        "command": "open-browser-with-url",
        "arguments": [editable_info["bundleId"], editable_info["activeUrl"]],
    }
    return dispatch(payload)


def re_write_text_to_editable(editable_info: dict, text_file: str) -> bool:
    result = re_open_browser_with_url(editable_info)
    assert "status" in result, "status must be present"
    if result["status"] != "ok":
        return False

    result = focus_editable(editable_info["editableId"])
    assert "status" in result, "status must be present"
    if result["status"] != "ok":
        return False

    result = set_editable_text(text_file, editable_info["contentEditable"])
    assert "status" in result, "status must be present"
    if result["status"] != "ok":
        return False

    return True


def last_resort(text_file: str):
    make_symbolic_file(text_file, "error")
    error_json = str(Path(text_file).parent) + "/error.json"
    error_text = str(Path(text_file).parent) + "/error.txt"
    display_dialog(
        f"""
Export failed.

Your edits have not been lost.

Please check the following files:

{error_json}

{error_text}

Please handle any further issues manually.
        """,
        opt="ok only",
    )
