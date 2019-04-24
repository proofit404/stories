from . import function
from .._return import Success


class AsyncBeginningOfStory(function.BeginningOfStory):
    async def __call__(self, ctx):
        return Success()


class AsyncEndOfStory(function.EndOfStory):
    async def __call__(self, ctx):
        return Success()
