from collections.abc import Callable
from typing import Protocol

from stories import Actor as Actor
from stories import initiate as initiate
from stories import Story as Story


def run(story: Story, state: object) -> None:
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


class Interface(Protocol):
    Actor: type[Actor]
    initiate: type[initiate]
    Story: type[Story]

    @staticmethod
    def run(story: Story, state: object) -> None:
        ...

    @staticmethod
    def normal_method(self: object, state: object) -> None:
        ...

    @staticmethod
    def assign_method(
        attribute: str, value: object
    ) -> Callable[[object, object], None]:
        ...

    @staticmethod
    def assert_method(
        attribute: str, value: object
    ) -> Callable[[object, object], None]:
        ...

    @staticmethod
    def append_method(
        attribute: str, value: object
    ) -> Callable[[object, object], None]:
        ...

    @staticmethod
    def error_method(message: str) -> Callable[[object, object], None]:
        ...

    StepError: type[StepError]
