import os
import sys
import json
import traceback
from typing import Any, Optional
import shutil
from datetime import datetime


LEVELS = {
    "error": 0,
    "warn": 1,
    "info": 2,
    "debug": 3,
    "trace": 4,
}
_write_stream = None
LOG_FILE = ""
LOG_LEVEL = 4


def get_log_file() -> str:
    raw = os.getenv("WENVI_LOG_FILE", "none")
    try:
        fixed = raw.encode("latin-1").decode("utf-8")
    except UnicodeError:
        fixed = raw
    open("/tmp/wenvi_log_file", "a", encoding="utf-8").write(
        f"LOG_FILE fixed : {fixed}\n"
    )
    return fixed


def write(msg: str) -> None:
    if _write_stream:
        _write_stream.write(msg + "\n")
        _write_stream.flush()
    else:
        sys.stderr.write(msg + "\n")
        sys.stderr.flush()


def stringify(value: Any) -> str:
    if isinstance(value, str):
        return value
    try:
        return json.dumps(value, ensure_ascii=False, indent=2)
    except Exception:
        return str(value)


def format_message(level: str, args: tuple[Any, ...], trace: Optional[str]) -> str:
    body = " ".join(stringify(a) for a in args)
    msg = f"[{level.upper()}] {body}"
    if trace:
        msg += "\n" + trace
    return msg


def get_trace(skip: int = 2) -> str:
    stack = traceback.format_stack()
    return "".join(stack[:-skip])


def _log(level: str, with_trace: bool, *args: Any) -> None:
    if LEVELS[level] > LOG_LEVEL:
        return

    if "cannot" in " ".join(stringify(a) for a in args):
        write("HOGE")
        write("".join(traceback.format_stack()))
        with_trace = True

    trace = get_trace(5) if with_trace else None

    now = datetime.now()
    timestamp = now.strftime("%M:%S.%f")[:-3]

    message = f"[{timestamp}][py]{format_message(level, args, trace)}"

    write(message)


class _Logger:
    def error(self, *a: Any) -> None:
        _log("error", False, *a)

    def warn(self, *a: Any) -> None:
        _log("warn", False, *a)

    def info(self, *a: Any) -> None:
        _log("info", False, *a)

    def debug(self, *a: Any) -> None:
        _log("debug", False, *a)

    def trace(self, *a: Any) -> None:
        _log("trace", True, *a)

    def set_log_file(self, new_path: str) -> None:
        global _write_stream, LOG_FILE

        LOG_FILE = new_path
        if _write_stream:
            _write_stream.close()
            _write_stream = None
        _write_stream = open(LOG_FILE, "a", encoding="utf-8")

    def get_log_file(self) -> str:
        global LOG_FILE
        return LOG_FILE

    def switch_log_file(self, new_path: str) -> None:
        global _write_stream, LOG_FILE

        if _write_stream:
            _write_stream.close()
            _write_stream = None

        if LOG_FILE != "none" and os.path.exists(LOG_FILE):
            if os.path.abspath(LOG_FILE) != os.path.abspath(new_path):
                shutil.move(LOG_FILE, new_path)

        LOG_FILE = new_path
        os.environ["WENVI_LOG_FILE"] = LOG_FILE

        _write_stream = open(LOG_FILE, "a", encoding="utf-8")

    def init(self) -> None:
        global _write_stream, LOG_FILE, logger, LOG_LEVEL
        log_level_name = os.getenv("WENVI_LOG_LEVEL", "info")
        LOG_LEVEL = LEVELS.get(log_level_name, LEVELS["info"])
        LOG_FILE = get_log_file()
        _write_stream = None
        if LOG_FILE != "none":
            _write_stream = open(LOG_FILE, "a", encoding="utf-8")


logger = _Logger()
