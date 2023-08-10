from stories.steps import Steps


class _StoryType(type):
    def __prepare__(class_name, bases):
        return {"I": Steps()}


class Story(metaclass=_StoryType):
    """Business process specification.

    Use sentences from business domain to express its steps.

    """

    def __call__(self, state):
        for step in self.I.__steps__:
            method = getattr(self, step)
            method(state)
