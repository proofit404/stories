from types import SimpleNamespace

import pytest


def functions():
    def run(story, state):
        return story(state)

    def normal_method(self, state):
        ...

    def assign_method(attribute, value):
        def method(self, state):
            setattr(state, attribute, value)

        return method

    def assert_method(attribute, value):
        def method(self, state):
            assert getattr(state, attribute) == value

        return method

    def append_method(attribute, value):
        def method(self, state):
            getattr(state, attribute).append(value)

        return method

    def error_method(message):
        def method(self, state):
            raise StepError(message)

        return method

    class StepError(Exception):
        ...

    return SimpleNamespace(
        run=run,
        normal_method=normal_method,
        assign_method=assign_method,
        assert_method=assert_method,
        append_method=append_method,
        error_method=error_method,
        StepError=StepError,
    )


def coroutines():
    import asyncio

    def run(story, state):
        return asyncio.run(story(state))

    async def normal_method(self, state):
        ...

    def assign_method(attribute, value):
        async def method(self, state):
            setattr(state, attribute, value)

        return method

    def assert_method(attribute, value):
        async def method(self, state):
            assert getattr(state, attribute) == value

        return method

    def append_method(attribute, value):
        async def method(self, state):
            getattr(state, attribute).append(value)

        return method

    def error_method(message):
        async def method(self, state):
            raise StepError(message)

        return method

    class StepError(Exception):
        ...

    return SimpleNamespace(
        run=run,
        normal_method=normal_method,
        assign_method=assign_method,
        assert_method=assert_method,
        append_method=append_method,
        error_method=error_method,
        StepError=StepError,
    )


@pytest.fixture(params=[functions(), coroutines()])
def s(request):
    return request.param
