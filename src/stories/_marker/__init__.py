from .function import BeginningOfStory, EndOfStory


try:
    from .coroutine import AsyncBeginningOfStory, AsyncEndOfStory
# Current Python version has no async/await support
except SyntaxError:
    pass
