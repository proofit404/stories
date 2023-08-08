from collections.abc import Callable
from collections.abc import Coroutine
from types import SimpleNamespace
from typing import Any

import pytest
from _pytest.fixtures import SubRequest


def functions() -> SimpleNamespace:
    from stories import Story, initiate, Actor

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

    return SimpleNamespace(
        Story=Story,
        initiate=initiate,
        Actor=Actor,
        run=run,
        normal_method=normal_method,
        assign_method=assign_method,
        assert_method=assert_method,
        append_method=append_method,
        error_method=error_method,
        StepError=StepError,
        BaseStory=Story,
    )


def coroutines() -> SimpleNamespace:
    import asyncio
    from aiostories import Story, initiate, Actor

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

    return SimpleNamespace(
        Story=Story,
        initiate=initiate,
        Actor=Actor,
        run=run,
        normal_method=normal_method,
        assign_method=assign_method,
        assert_method=assert_method,
        append_method=append_method,
        error_method=error_method,
        StepError=StepError,
    )


@pytest.fixture(params=[functions(), coroutines()])
def s(request: SubRequest) -> Any:
    return request.param
