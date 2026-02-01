from typing import TypedDict, Sequence

from platforms.macos.invoke_osa import invoke_osa
from shared.utils import assert_
from global_ import GLOBAL


class EditableInfo(TypedDict):
    bundleId: str
    appName: str
    activeUrl: str


def entry(arguments_object: Sequence = ()) -> dict:
    assert_(len(arguments_object) == 0, "does not accept any arguments")

    raw_output = invoke_osa("get-editable-info")
    editable_info = parse_editable_info(raw_output)

    set_global_app_name(editable_info["appName"])

    return {
        "status": "ok",
        **editable_info,
    }


def parse_editable_info(output: str) -> EditableInfo:
    bundle_id, app_name, active_url = output.strip().split("\t")

    return {
        "bundleId": bundle_id,
        "appName": app_name,
        "activeUrl": active_url,
    }


def set_global_app_name(app_name: str) -> None:
    GLOBAL["APP_NAME"] = app_name
