import subprocess
from shared.utils import assert_
from shared.logger import logger


def entry(arguments_object: list[str]) -> dict:
    assert_(len(arguments_object) == 2, "need bundleId and url arguments")
    open_url_with_bundle_id(arguments_object)
    return {"status": "ok"}


def open_url_with_bundle_id(arguments: list[str]) -> None:
    logger.debug(["open-browser/bundleId, URL : ", arguments])
    bundle_id = arguments[0]
    url = arguments[1]
    subprocess.run(
        ["open", "-b", bundle_id, url],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
