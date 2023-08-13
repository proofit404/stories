from typing import ClassVar

from stories.story import Steps
from stories.story import StoryType


class Story(metaclass=StoryType):
    """Business process specification.

    Use sentences from business domain to express its steps.

    """

    I: ClassVar[Steps]

    async def __call__(self, state) -> None:
        for method in self.I(self):
            await method(state)
