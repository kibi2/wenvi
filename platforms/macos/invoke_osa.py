from __future__ import annotations

import subprocess
from pathlib import Path
from typing import List

from shared.logger import logger
from shared.utils import DomainError
from global_ import GLOBAL


def invoke_osa(command: str, args: List[str] | None = None) -> str:
    """
    Execute AppleScript via osascript.
    """
    if args is None:
        args = []

    _assert_app_name_available()

    apple_script = _load_resolved_apple_script()

    return _execute_osa_script(
        apple_script=apple_script,
        command=command,
        args=args,
    )


def _assert_app_name_available() -> None:
    app_name = GLOBAL["APP_NAME"]

    if not isinstance(app_name, str) or not app_name.strip():
        raise DomainError("App name is not exist.")


def _load_resolved_apple_script() -> str:
    template = _load_apple_script_template()
    return _inject_app_name(template, GLOBAL["APP_NAME"])


def _load_apple_script_template() -> str:
    current_dir = Path(__file__).resolve().parent
    script_path = current_dir / "apple" / "main.applescript"

    return script_path.read_text(encoding="utf-8")


def _inject_app_name(script: str, app_name: str) -> str:
    return script.replace("__APP_NAME__", app_name)


def _execute_osa_script(
    *,
    apple_script: str,
    command: str,
    args: List[str],
) -> str:
    logger.debug(f"[start {command}]:len(args)=" + str(len(args)))
    process = _spawn_osa_process(command, args)

    stdout, stderr = process.communicate(apple_script)

    if stderr:
        raise _parse_osa_error(stderr)

    logger.debug(f"[end   {command}]:stdout=" + repr(stdout))
    return stdout


def _spawn_osa_process(command: str, args: List[str]) -> subprocess.Popen[str]:
    return subprocess.Popen(
        ["osascript", "-", command, *args],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def _parse_osa_error(stderr: str) -> Exception:
    message = stderr.strip()

    if "[warn]" in message:
        return RuntimeError(message)

    return RuntimeError(message)
