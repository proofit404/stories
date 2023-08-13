from __future__ import annotations

from collections.abc import Callable
from collections.abc import Iterable
from typing import ClassVar


class Steps:
    def __init__(self) -> None:
        self.__steps__: list[str] = []

    def __getattr__(self, name: str) -> None:
        self.__steps__.append(name)

    def __call__(self, story: Story) -> Iterable[Callable[[object], None]]:
        for step in self.__steps__:
            yield getattr(story, step)


class StoryType(type):
    @classmethod
    def __prepare__(cls, name, bases) -> dict[str, Steps]:
        return {"I": Steps()}


class Story(metaclass=StoryType):
    """Business process specification.

    Use sentences from business domain to express its steps.

    """

    I: ClassVar[Steps]

    def __call__(self, state) -> None:
        for method in self.I(self):
            method(state)
