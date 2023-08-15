from collections.abc import Callable

from stories import Actor as actor_class
from stories import initiate
from stories import Story as story_class


def run(story: story_class, state: object) -> None:
    return story(state)


def normal_method(self: object, state: object) -> None:
    ...


def assign_method(attribute: str, value: object) -> Callable[[object, object], None]:
    def method(self: object, state: object) -> None:
        setattr(state, attribute, value)

    return method


def assert_method(attribute: str, value: object) -> Callable[[object, object], None]:
    def method(self: object, state: object) -> None:
        x: object = getattr(state, attribute)
        assert x == value

    return method


def append_method(attribute: str, value: object) -> Callable[[object, object], None]:
    def method(self: object, state: object) -> None:
        x: list[object] = getattr(state, attribute)
        x.append(value)

    return method


def error_method(message: str) -> Callable[[object, object], None]:
    def method(self: object, state: object) -> None:
        raise StepError(message)

    return method


class StepError(Exception):
    ...
