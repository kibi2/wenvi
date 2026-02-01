from python.platform.platform_dispatcher import dispatch
from shared.utils import assert_
from platforms.macos.invoke_osa import invoke_osa


def entry(arguments_object: list[str]) -> dict:
    assert_(len(arguments_object) == 1, "need active URL argument")
    activate_browser_tab(arguments_object)
    return {"status": "ok"}


def activate_browser_tab(arguments_object: list[str]) -> None:
    invoke_osa("activate-browser-tab", arguments_object)
