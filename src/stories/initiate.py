from dataclasses import make_dataclass
from inspect import isclass
from typing import TypeVar

from stories.exceptions import StoryError
from stories.story import Story

T = TypeVar("T")


class Initiate:
    """Create story with all steps required in constructor argument."""

    def __init__(self, bases: tuple[type[Story]]) -> None:
        self.bases = bases

    def __call__(self, cls: type[Story]) -> type[Story]:
        self.check_bases(cls)
        self.check_steps(cls)
        self.check_init(cls)
        result = make_dataclass(cls.__name__, cls.I.__steps__)
        cls.__init__ = result.__init__
        return cls

    def check_bases(self, cls: type[Story]) -> None:
        if not (isclass(cls) and issubclass(cls, self.bases)):
            raise StoryError("@initiate can decorate Story subclasses only")

    def check_steps(self, cls: type[Story]) -> None:
        for attrname in cls.I.__steps__:
            if attrname in cls.__dict__:
                raise StoryError(
                    "Story decorated by @initiate can not have step methods"
                )

    def check_init(self, cls: type[Story]) -> None:
        if "__init__" in cls.__dict__:
            raise StoryError(
                "Story decorated by @initiate can not have constructor defined"
            )
