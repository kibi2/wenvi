from typing import List, Any
import json

from platforms.macos.invoke_osa import invoke_osa
from shared.utils import assert_


def entry(arguments_object: List[str]) -> Any:
    """
    Execute JavaScript in browser via AppleScript.
    arguments_object: list of length 1 [javascript_source]
    """
    assert_(len(arguments_object) == 1, "need javascript source argument")

    javascript_source = arguments_object[0]
    stdout = invoke_osa("execute-javascript", [javascript_source])

    return parse_json(stdout)


def parse_json(stdout: str) -> Any:
    return json.loads(stdout)
