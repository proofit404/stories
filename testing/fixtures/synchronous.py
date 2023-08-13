from stories import Actor  # noqa: F401
from stories import initiate  # noqa: F401
from stories import Story  # noqa: F401


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
