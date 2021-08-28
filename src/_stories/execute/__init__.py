from asyncio import iscoroutinefunction
from functools import partial
from types import MethodType

from _stories.execute import coroutine
from _stories.execute import function


class _Executor:
    def __init__(self, steps):
        self.steps = steps

    def __get__(self, instance, klass):
        if instance is None:
            return self
        first_step = getattr(instance, self.steps[0])
        if isinstance(first_step, MethodType):
            step = first_step.__func__
        else:
            step = first_step.__call__.func
        if iscoroutinefunction(step):
            func = coroutine._execute
        else:
            func = function._execute
        return partial(func, self.steps, instance)
