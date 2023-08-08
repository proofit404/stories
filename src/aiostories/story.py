from typing import TypeVar

from stories.steps import Steps
from stories.story import _StoryType

T = TypeVar("T", bound=object)


class Story(metaclass=_StoryType):
    """Business process specification.

    Use sentences from business domain to express its steps.

    """

    I: Steps

    async def __call__(self, state: T) -> None:
        for step in self.I.__steps__:
            method = getattr(self, step)
            await method(state)
