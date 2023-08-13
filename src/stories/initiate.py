from dataclasses import make_dataclass
from inspect import isclass
from typing import TypeVar

from stories.exceptions import StoryError
from stories.story import Story


T = TypeVar("T")


def initiate(cls: T) -> T:
    """Create story with all steps required in constructor argument."""
    _check_bases(cls)
    _check_steps(cls)
    _check_init(cls)
    return make_dataclass(
        cls.__name__,
        cls.I.__steps__,
        namespace={"I": cls.I, "__call__": cls.__call__},
    )


def _check_bases(cls: type[Story]) -> None:
    if not (isclass(cls) and issubclass(cls, Story)):
        raise StoryError("@initiate can decorate Story subclasses only")


def _check_steps(cls: type[Story]) -> None:
    for attrname in cls.I.__steps__:
        if attrname in cls.__dict__:
            raise StoryError("Story decorated by @initiate can not have step methods")


def _check_init(cls: type[Story]) -> None:
    if "__init__" in cls.__dict__:
        raise StoryError(
            "Story decorated by @initiate can not have constructor defined"
        )
