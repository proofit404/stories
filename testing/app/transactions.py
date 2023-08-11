from collections.abc import Callable
from typing import TypeVar


T = TypeVar("T")


def atomic(f: Callable[..., T]) -> Callable[..., T]:
    def wrapper(*args, **kwargs) -> T:
        start_transaction()
        result = f(*args, **kwargs)
        end_transaction()
        return result

    return wrapper


def start_transaction() -> None:
    print("BEGIN TRANSACTION;")


def end_transaction() -> None:
    print("COMMIT TRANSACTION;")


def cancel_transaction() -> None:
    print("ROLLBACK TRANSACTION;")
