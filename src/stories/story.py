from typing import TypeVar


Fn = TypeVar("Fn")


def story(fn: Fn) -> Fn:
    return fn
