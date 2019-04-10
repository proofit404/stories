import inspect
from .function import execute as execute_sync
from .coroutine import execute as execute_async


def execute(runner, ctx, history, methods):
    if any(inspect.iscoroutinefunction(item[0]) for item in methods):
        return execute_async(runner, ctx, history, methods)
    else:
        return execute_sync(runner, ctx, history, methods)