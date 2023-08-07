from dataclasses import make_dataclass
from inspect import isclass

from _stories.exceptions import StoryError
from _stories.story import Story


def initiate(cls):
    """Create story with all steps required in constructor argument."""
    _check_bases(cls)
    _check_steps(cls)
    _check_init(cls)
    return make_dataclass(
        cls.__name__, cls.__call__.steps, namespace={"__call__": cls.__call__}
    )


def _check_bases(cls):
    if not (isclass(cls) and issubclass(cls, Story)):
        raise StoryError("@initiate can decorate Story subclasses only")


def _check_steps(cls):
    for attrname in cls.__call__.steps:
        if attrname in cls.__dict__:
            raise StoryError("Story decorated by @initiate can not have step methods")


def _check_init(cls):
    if "__init__" in cls.__dict__:
        raise StoryError(
            "Story decorated by @initiate can not have constructor defined"
        )
