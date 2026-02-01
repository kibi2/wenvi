from typing import Literal, Optional


NgResultStatus = Literal["error", "warn"]


class DomainError(Exception):
    def __init__(self, message: str, status: NgResultStatus = "error"):
        super().__init__(message)
        self.status: NgResultStatus = status


def assert_(
    condition: bool,
    message: str,
    status: NgResultStatus = "error",
) -> None:
    if not condition:
        raise DomainError(message, status)


def normalize_text(value: Optional[object]) -> str:
    return "" if value is None else str(value)


def head_lines(text: str, n: int = 5) -> str:
    return "\n".join(text.splitlines()[:n])
