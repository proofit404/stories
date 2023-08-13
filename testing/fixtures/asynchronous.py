import asyncio
from collections.abc import Awaitable
from collections.abc import Callable
from typing import Protocol

from aiostories import Actor as Actor
from aiostories import initiate as initiate
from aiostories import Story as Story


def run(story: Story, state: object) -> None:
    return asyncio.run(story(state))


async def normal_method(self: object, state: object) -> None:
    ...


def assign_method(
    attribute: str, value: object
) -> Callable[[object, object], Awaitable[None]]:
    async def method(self: object, state: object) -> None:
        setattr(state, attribute, value)

    return method


def assert_method(
    attribute: str, value: object
) -> Callable[[object, object], Awaitable[None]]:
    async def method(self: object, state: object) -> None:
        x: object = getattr(state, attribute)
        assert x == value

    return method


def append_method(
    attribute: str, value: object
) -> Callable[[object, object], Awaitable[None]]:
    async def method(self: object, state: object) -> None:
        x: list[object] = getattr(state, attribute)
        x.append(value)

    return method


def error_method(message: str) -> Callable[[object, object], Awaitable[None]]:
    async def method(self: object, state: object) -> None:
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
    async def normal_method(self: object, state: object) -> None:
        ...

    @staticmethod
    def assign_method(
        attribute: str, value: object
    ) -> Callable[[object, object], Awaitable[None]]:
        ...

    @staticmethod
    def assert_method(
        attribute: str, value: object
    ) -> Callable[[object, object], Awaitable[None]]:
        ...

    @staticmethod
    def append_method(
        attribute: str, value: object
    ) -> Callable[[object, object], Awaitable[None]]:
        ...

    @staticmethod
    def error_method(message: str) -> Callable[[object, object], Awaitable[None]]:
        ...

    StepError: type[StepError]
