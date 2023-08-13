import asyncio
from collections.abc import Callable
from collections.abc import Coroutine
from typing import Any

from aiostories import Actor  # noqa: F401
from aiostories import initiate  # noqa: F401
from aiostories import Story


def run(story: Story, state: object) -> Any:
    return asyncio.get_event_loop().run_until_complete(story(state))


async def normal_method(self: object, state: object) -> None:
    ...


def assign_method(
    attribute: str, value: Any
) -> Callable[[object, object], Coroutine[Any, Any, None]]:
    async def method(self: object, state: object) -> None:
        setattr(state, attribute, value)

    return method


def assert_method(
    attribute: str, value: Any
) -> Callable[[object, object], Coroutine[Any, Any, None]]:
    async def method(self: object, state: object) -> None:
        assert getattr(state, attribute) == value

    return method


def append_method(
    attribute: str, value: Any
) -> Callable[[object, object], Coroutine[Any, Any, None]]:
    async def method(self: object, state: object) -> None:
        getattr(state, attribute).append(value)

    return method


def error_method(
    message: str,
) -> Callable[[object, object], Coroutine[Any, Any, None]]:
    async def method(self: object, state: object) -> None:
        raise StepError(message)

    return method


class StepError(Exception):
    ...
