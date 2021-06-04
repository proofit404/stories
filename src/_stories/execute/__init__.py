from asyncio import iscoroutinefunction
from functools import partial

from _stories.execute import coroutine
from _stories.execute import function


def _get_executor(steps, namespace):
    if iscoroutinefunction(namespace[steps[0]]):
        func = coroutine._execute
    else:
        func = function._execute
    return _Executor(func, steps)


class _Executor:
    def __init__(self, func, steps):
        self.func = func
        self.steps = steps

    def __get__(self, instance, klass):
        return partial(self.func, self.steps, instance)
