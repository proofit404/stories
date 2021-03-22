from asyncio import iscoroutinefunction

from _stories.execute import coroutine
from _stories.execute import function


def _get_executor(method):
    if iscoroutinefunction(method):
        return coroutine._execute
    else:
        return function._execute
