import asyncio
from collections.abc import Awaitable
from collections.abc import Callable

from aiostories import Actor as actor_class
from aiostories import initiate
from aiostories import Story as story_class


def run(story: story_class, state: object) -> None:
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
