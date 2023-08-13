from typing import ClassVar

from stories.steps import Steps


class _StoryType(type):
    @classmethod
    def __prepare__(cls, name, bases) -> dict[str, Steps]:
        return {"I": Steps()}


class Story(metaclass=_StoryType):
    """Business process specification.

    Use sentences from business domain to express its steps.

    """

    I: ClassVar[Steps]

    def __call__(self, state) -> None:
        for method in self.I(self):
            method(state)
