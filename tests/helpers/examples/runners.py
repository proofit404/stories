import importlib

import pytest

import _stories.mounted


_stories.mounted.instrumented = False

origin_call = _stories.mounted.MountedStory.__call__
origin_run = _stories.mounted.MountedStory.run


def instrument(method):
    def wrapper(*args, **kwargs):
        if not _stories.mounted.instrumented:
            raise Exception("Use 'r' fixture to run the story")  # pragma: no cover
        return method(*args, **kwargs)

    return wrapper


_stories.mounted.MountedStory.__call__ = instrument(origin_call)
_stories.mounted.MountedStory.run = instrument(origin_run)


class Function:
    def __init__(self, story):
        self.story = story

    def __call__(self, *args, **kwargs):
        _stories.mounted.instrumented = True
        try:
            return self.story(*args, **kwargs)
        finally:
            _stories.mounted.instrumented = False

    @staticmethod
    def import_module(module_name):
        return importlib.import_module(module_name + ".functions")

    @staticmethod
    def skip_if_function():
        pytest.skip("The test is not intended to check functions")


class Coroutine:
    def __init__(self, story):
        self.story = story

    def __call__(self, *args, **kwargs):
        import asyncio

        _stories.mounted.instrumented = True
        try:
            c = self.story(*args, **kwargs)
        finally:
            _stories.mounted.instrumented = False
        if not asyncio.iscoroutine(c):
            raise Exception("A coroutine executor expected")  # pragma: no cover
        try:
            c.send(None)
        except StopIteration as error:
            return error.value
        else:
            raise Exception("A coroutine does not return")  # pragma: no cover

    @staticmethod
    def import_module(module_name):
        return importlib.import_module(module_name + ".coroutines")

    @staticmethod
    def skip_if_function():
        pass


runners = {"function": Function, "coroutine": Coroutine}
