from stories.story import _StoryType


class Story(metaclass=_StoryType):
    """Business process specification.

    Use sentences from business domain to express its steps.

    """

    async def __call__(self, state):
        for step in self.I.__steps__:
            method = getattr(self, step)
            await method(state)
