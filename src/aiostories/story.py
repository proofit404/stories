from typing import ClassVar

from stories.steps import Steps
from stories.story import _StoryType


class Story(metaclass=_StoryType):
    """Business process specification.

    Use sentences from business domain to express its steps.

    """

    I: ClassVar[Steps]

    async def __call__(self, state) -> None:
        for method in self.I(self):
            await method(state)
