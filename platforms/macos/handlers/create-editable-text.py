import os
import time
import json
import shutil
import subprocess
from platforms.macos.invoke_osa import invoke_osa
from python.domain.utils import get_js_code
from shared.utils import assert_
from shared.logger import logger


def entry(arguments_object: list = []) -> dict:
    assert_(
        len(arguments_object) == 2, "need text file name, isContentEditable argument"
    )
    isContentEditable = arguments_object[1] == "true"
    if isContentEditable:
        logger.debug(" CONTENT EDITABLE ")
        create_text_file(arguments_object[0])
    else:
        editable_text = get_text()["text"]
        logger.debug(["[get_text]: ", editable_text])
        write_text_file(arguments_object[0], editable_text)
    return {
        "status": "ok",
    }


def get_text() -> dict[str, str]:
    files = ["#browser/editable-core.js", "#browser/get-editable-text.js"]
    js_code = get_js_code(files, {})
    return json.loads(invoke_osa("execute-javascript", [js_code]))


def write_text_file(text_file: str, editable_text) -> None:
    with open(text_file, "w", encoding="utf-8") as f:
        f.write(editable_text)


def create_text_file(text_file: str) -> None:
    subprocess.run(
        ["open", "-g", f"hammerspoon://cmd_ac_safe"],
        check=True,
    )
    _TEXT_FILE_PATH_ = "/tmp/wenvi_hammerspoon.txt"
    while not os.path.exists(_TEXT_FILE_PATH_):
        time.sleep(0.01)
    shutil.move(_TEXT_FILE_PATH_, text_file)
