from typing import Protocol

from stories import Actor
from stories import initiate
from stories import Story


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


class Interface(Protocol):
    Actor: type[Actor]
    initiate: type[initiate]
    Story: type[Story]

    def run(story: type[Story], state: object):
        ...

    def normal_method(self, state):
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
