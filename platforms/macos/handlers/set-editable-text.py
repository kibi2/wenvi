import subprocess
import json
from urllib.parse import quote
from shared.utils import assert_
from python.domain.utils import get_js_code
from platforms.macos.invoke_osa import invoke_osa
from shared.logger import logger


def entry(arguments_object: list[str]) -> dict:
    assert_(
        len(arguments_object) == 2, "need editable text, isContentEditable argument"
    )
    editable_text = arguments_object[0]
    isContentEditable = arguments_object[1] == "true"
    if isContentEditable:
        logger.debug(" CONTENT EDITABLE ")
        update_editable_text(editable_text)
    else:
        result = set_text(editable_text)
        logger.debug(result)
    return {"status": "ok"}


def update_editable_text(editable_text: str) -> None:
    encoded = quote(editable_text, safe="")
    logger.debug(["encoded text:", encoded])
    subprocess.run(
        ["open", "-g", f"hammerspoon://cmd_av_safe?text={encoded}"],
        check=True,
    )


def set_text(editable_text) -> dict[str, str]:
    files = ["#browser/editable-core.js", "#browser/set-editable-text.js"]
    logger.debug(["[set_text]: ", editable_text])
    js_code = get_js_code(files, {"text": editable_text})
    result = invoke_osa("execute-javascript", [js_code])
    logger.debug(result)
    return json.loads(result)
