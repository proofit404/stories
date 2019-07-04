from typing import Optional

from ._return import Success
from ._types import AbstractContext, MethodResult


class BeginningOfStory(object):
    def __init__(self, cls_name, name):
        # type: (str, str) -> None
        self.cls_name = cls_name
        self.name = name
        self.parent_name = None  # type: Optional[str]
        self.same_object = None  # type: Optional[bool]

    def __call__(self, ctx):
        # type: (AbstractContext) -> MethodResult
        return Success()

    @property
    def __name__(self):
        # type: () -> str
        if self.parent_name is None:
            return self.cls_name + "." + self.name
        elif self.same_object:
            return self.parent_name
        else:
            return self.parent_name + " (" + self.cls_name + "." + self.name + ")"

    def set_parent(self, parent_name, same_object):
        # type: (Optional[str], bool) -> None
        self.parent_name = parent_name
        self.same_object = same_object


class EndOfStory(object):
    def __init__(self, is_empty):
        # type: (bool) -> None
        self.is_empty = is_empty

    def __call__(self, ctx):
        # type: (AbstractContext) -> MethodResult
        return Success()

    __name__ = "end_of_story"
