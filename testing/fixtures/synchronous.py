from collections.abc import Callable
from typing import Any

from stories import Actor  # noqa: F401
from stories import initiate  # noqa: F401
from stories import Story


def run(story: Story, state: object) -> Any:
    return story(state)


def normal_method(self: object, state: Story) -> None:
    ...


def assign_method(attribute: str, value: Any) -> Callable[[object, object], None]:
    def method(self: object, state: object) -> None:
        setattr(state, attribute, value)

    return method


def assert_method(attribute: str, value: Any) -> Callable[[object, object], None]:
    def method(self: object, state: object) -> None:
        assert getattr(state, attribute) == value

    return method


def append_method(attribute: str, value: Any) -> Callable[[object, object], None]:
    def method(self: object, state: object) -> None:
        getattr(state, attribute).append(value)

    return method


def error_method(message: str) -> Callable[[object, object], None]:
    def method(self: object, state: object) -> None:
        raise StepError(message)

    return method


class StepError(Exception):
    ...
