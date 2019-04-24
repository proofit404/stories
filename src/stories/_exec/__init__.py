import inspect
from . import function, coroutine


def execute(runner, ctx, history, methods):
    # Method can be anything callable
    if inspect.iscoroutinefunction(methods[0][0].__call__):
        return coroutine.execute(runner, ctx, history, methods)
    else:
        return function.execute(runner, ctx, history, methods)
