#!/usr/bin/env python3
import os
import time
import json
import shutil
from typing import Optional
from pathlib import Path
from datetime import datetime
from shared.logger import logger
from python.domain.utils import execute_js_in_browser
from python.domain.utils import make_symbolic_file
from python.domain.utils import save_app_info
from config.config import get_config, get_data_home
from python.platform.platform_contract import DispatchResult
from python.platform.platform_contract import DispatchRequest
from python.platform.platform_dispatcher import dispatch
from python.domain.utils import display_dialog


def read_form() -> None:
    result = get_editable_info()
    logger.debug(["[getEditableInfo]: ", result])
    editable_info = parse_editable_info(result)
    editable = read_editable_from_editable()
    exit_if_no_editable(editable)
    if not confirm_double_boot(editable):
        return
    logger.debug(["[read_editable_from_editable]", editable])
    text_file = prepare_json_and_text_files(editable_info, editable)
    create_text_file(text_file, editable)
    make_symbolic_file(text_file, "last")
    cmd = load_editor_command(text_file)
    launch_editor(cmd)


def get_editable_info() -> DispatchResult:
    json_payload: DispatchRequest = {"command": "get-editable-info"}
    return dispatch(json_payload)


def parse_editable_info(result: DispatchResult) -> DispatchResult:
    if result.get("status") != "ok":
        logger.info(result)
        logger.warn("Browser is not activated.")
        exit(1)
    return result


def read_editable_from_editable() -> DispatchResult:
    files = ["#browser/editable-core.js", "#browser/editable-select.js"]
    return execute_js_in_browser(files, {})


def exit_if_no_editable(result: DispatchResult) -> None:
    if result.get("status") != "ok":
        logger.info(result)
        logger.warn("There is no editable area")
        exit(1)


def prepare_json_and_text_files(
    editable_info: DispatchResult, editable: DispatchResult
) -> str:
    assert "hostName" in editable, "hostName must be present"
    assert "title" in editable, "title must be present"
    assert "editableId" in editable, "editableId must be present"
    assert "contentEditable" in editable, "contentEditable must be present"
    assert "bundleId" in editable_info, "bundleId must be present"
    assert "appName" in editable_info, "appName must be present"
    assert "activeUrl" in editable_info, "activeUrl must be present"
    data_home = Path(get_data_home()) / editable["hostName"]
    data_home.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    base_name = safe_filename(f"{timestamp}_{editable['title']}.wenvi")
    text_file = data_home / f"{base_name}.txt"
    json_file = data_home / f"{base_name}.json"
    log_file = data_home / f"{base_name}.log"
    logger.switch_log_file(str(log_file))
    logger.debug(["[prepareJson]: ", text_file])
    output = {
        "schema": 1,
        "status": "open",
        "bundleId": editable_info["bundleId"],
        "appName": editable_info["appName"],
        "activeUrl": editable_info["activeUrl"],
        "editableId": editable["editableId"],
        "hostName": editable["hostName"],
        "contentEditable": editable["contentEditable"],
    }
    logger.debug({"jsonFile": str(json_file), "text": output})
    save_app_info(str(text_file), output)
    return str(text_file)


def create_text_file(text_file: str, editable) -> None:
    json_payload: DispatchRequest = {
        "command": "create-editable-text",
        "arguments": [text_file, editable["contentEditable"]],
    }
    dispatch(json_payload)


def safe_filename(title: str, max_bytes: int = 100) -> str:
    import re

    name = re.sub(r"[^\w\-_\. ]", "_", title.strip())
    if not name:
        name = "untitled"

    bytes_count = 0
    out = ""
    for ch in name:
        b = len(ch.encode("utf-8"))
        if bytes_count + b > max_bytes:
            break
        bytes_count += b
        out += ch
    return out.replace(" ", "_")


def load_editor_command(text_file: str) -> str:
    editor_cmd = "nvim {TEXT_FILE}"
    from_config = get_config().editor
    if from_config:
        editor_cmd = from_config
    return editor_cmd.replace("{TEXT_FILE}", text_file)


def launch_editor(cmd: str):
    from subprocess import Popen

    env = os.environ.copy()
    child = Popen(cmd, shell=True, env=env)
    return child


def confirm_double_boot(editable) -> bool:
    open_path = is_editable_open(editable)
    if open_path is None:
        return True
    result = display_dialog(
        f"""
This text input area appears to be already open in Wenvi.

Press OK to edit it here anyway,
or Cancel to continue editing in Wenvi.
        """
    )
    logger.debug("[confirm] result= ", result)
    assert "result" in result, "result must be present"
    return result["result"] == "ok"


def is_editable_open(editable: DispatchResult, n_latest: int = 5) -> Optional[Path]:
    assert "hostName" in editable, "hostName must be present"
    assert "title" in editable, "title must be present"
    data_home = Path(get_data_home()) / editable["hostName"]
    json_wild = f"*_{safe_filename(editable['title'])}.wenvi.json"
    candidates = sorted(
        data_home.glob(json_wild), key=lambda p: p.stat().st_mtime, reverse=True
    )

    for json_file in candidates[:n_latest]:
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            if data.get("status") == "open":
                return json_file
        except Exception:
            continue

    return None


if __name__ == "__main__":
    read_form()
