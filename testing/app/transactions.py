from collections.abc import Callable
from typing import TypeVar

from app.tools import log

RetType = TypeVar("RetType")


def atomic(f: Callable[..., RetType]) -> Callable[..., RetType]:
    """Manage transactions."""

    def wrapper(*args: object, **kwargs: object) -> RetType:
        start_transaction()
        result = f(*args, **kwargs)
        end_transaction()
        return result

    return wrapper


def start_transaction() -> None:
    """Perform database query."""
    log("BEGIN TRANSACTION;")


def end_transaction() -> None:
    """Perform database query."""
    log("COMMIT TRANSACTION;")


def cancel_transaction() -> None:
    """Perform database query."""
    log("ROLLBACK TRANSACTION;")
