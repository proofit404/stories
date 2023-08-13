import asyncio
from typing import Protocol

from aiostories import Actor
from aiostories import initiate
from aiostories import Story


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


class Interface(Protocol):
    Actor: type[Actor]
    initiate: type[initiate]
    Story: type[Story]

    def run(story: type[Story], state: object):
        ...

    async def normal_method(self, state):
        ...

    def assign_method(attribute, value):
        ...

    def assert_method(attribute, value):
        ...

    def append_method(attribute, value):
        ...

    def error_method(message):
        ...

    StepError: type[StepError]
