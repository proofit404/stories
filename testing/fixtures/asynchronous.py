import asyncio

from aiostories import Actor  # noqa: F401
from aiostories import initiate  # noqa: F401
from aiostories import Story  # noqa: F401


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
