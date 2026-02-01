from __future__ import annotations

import json
import os
import pathlib
from typing import Any, Dict, Iterable, List, Optional

from shared.logger import logger
from python.platform.platform_dispatcher import dispatch
from python.platform.platform_contract import DispatchResult
from python.platform.platform_contract import DispatchRequest
from typing import Mapping, Any, Iterable


def make_dispatch_request(
    command: str,
    arguments: Optional[List[str]] = None,
) -> DispatchRequest:
    return {
        "command": command,
        "arguments": arguments,
    }


def get_js_code(files: Iterable[str], args: Mapping[str, Any]) -> str:
    logger.debug(files)
    logger.debug(args)
    js_main = cat_browser_javascript(files)

    js_code = f"""
(function(args) {{
{js_main}
try {{
    return entry(args);
}} catch (exception) {{
    return JSON.stringify({{
        status: "error",
        message: exception.message,
    }});
}}
}})({json.dumps(args)});
"""
    return js_code


def execute_js_in_browser(
    files: Iterable[str], args: Mapping[str, Any]
) -> DispatchResult:
    return dispatch(
        make_dispatch_request(
            "execute-javascript",
            [get_js_code(files, args)],
        )
    )


def cat_browser_javascript(files: Iterable[str]) -> str:
    codes: List[str] = []

    for file in files:
        full_path = resolve_js_path(file)
        code = full_path.read_text(encoding="utf-8")
        codes.append(f"// ===== {file} =====\n{code}")

    return "\n\n".join(codes)


def resolve_js_path(file: str) -> pathlib.Path:
    if file.startswith("#"):
        file = file[1:]

    root = pathlib.Path(__file__).resolve().parents[2]
    return root / file


def display_dialog(message: str, opt: Optional[str] = None) -> DispatchResult:
    if opt is None:
        payload = make_dispatch_request(
            "display-dialog",
            [message],
        )
    else:
        payload = make_dispatch_request(
            "display-dialog",
            [message, opt],
        )

    return dispatch(payload)


def make_symbolic_file(text_file: str, base: str) -> None:
    text_path = pathlib.Path(text_file)
    json_path = text_path.with_suffix(".json")
    log_path = text_path.with_suffix(".log")

    dir_path = text_path.parent
    text_link = dir_path / f"{base}.txt"
    json_link = dir_path / f"{base}.json"
    log_link = dir_path / f"{base}.log"

    try:
        text_link.unlink(missing_ok=True)
        json_link.unlink(missing_ok=True)
        log_link.unlink(missing_ok=True)

        text_link.symlink_to(text_path)
        json_link.symlink_to(json_path)
        log_link.symlink_to(log_path)

    except Exception as exc:
        logger.error(str(exc))


def focus_editable(editable_id: str):
    files = [
        "#browser/editable-core.js",
        "#browser/editable-focus.js",
    ]
    return execute_js_in_browser(files, {"editableId": editable_id})


def set_editable_text(text_file: str, contentEditable: str) -> DispatchResult:
    editable_text = pathlib.Path(text_file).read_text(encoding="utf-8")
    return dispatch(
        make_dispatch_request(
            "set-editable-text",
            [editable_text, contentEditable],
        )
    )


def load_app_info(text_file: str) -> Dict[str, Any]:
    info_file = pathlib.Path(text_file).with_suffix(".json")
    if not info_file.exists():
        raise FileNotFoundError(f"editableInfoFile not found: {info_file}")

    editable_info = json.loads(info_file.read_text(encoding="utf-8"))

    if "appName" in editable_info:
        editable_info["appName"] = editable_info["appName"].replace("'", "")
    if "activeUrl" in editable_info:
        editable_info["activeUrl"] = editable_info["activeUrl"].replace("'", "")

    return editable_info


def save_app_info(text_file: str, contents: Dict[str, Any]) -> None:
    json_file = pathlib.Path(text_file).with_suffix(".json")
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(contents, f, ensure_ascii=False, indent=2)


def setStatus(text_file: str, status: str) -> None:
    editable_info = load_app_info(text_file)
    editable_info["status"] = status
    save_app_info(text_file, editable_info)
