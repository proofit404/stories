import typing

from _stories.context import Context
from _stories.returned import Success

class BeginningOfStory:
    def __init__(self, cls_name: str, name: str) -> None: ...
    @property
    def story_name(self) -> str: ...
    def set_parent(self, parent_name: str, same_object: bool) -> None: ...

class EndOfStory: ...

class Parallel:
    def __init__(self, calls: typing.List[typing.Callable], workers: int) -> None: ...
    def __call__(self, ctx: Context) -> Success: ...
    @property
    def story_name(self) -> str: ...