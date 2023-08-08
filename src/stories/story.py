from collections.abc import Mapping
from typing import Any
from typing import TypeVar

from stories.steps import Steps

T = TypeVar("T", bound=object)


class _StoryType(type):
    @classmethod
    def __prepare__(
        metacls, __name: str, __bases: tuple[type, ...], **kwds: Any
    ) -> Mapping[str, Steps]:
        return {"I": Steps()}


class Story(metaclass=_StoryType):
    """Business process specification.

    Use sentences from business domain to express its steps.

    """

    I: Steps

    def __call__(self, state: T) -> None:
        for step in self.I.__steps__:
            method = getattr(self, step)
            method(state)
