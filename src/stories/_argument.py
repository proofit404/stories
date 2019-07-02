from typing import Callable

from ._types import Arguments, Spec
from .exceptions import StoryDefinitionError


def arguments(*names):
    # type: (*str) -> Callable
    if not names:
        raise StoryDefinitionError("Story arguments can not be an empty list")

    if any(name for name in names if not isinstance(name, str)):
        message = "Story arguments can only be defined with string type"
        raise StoryDefinitionError(message)

    def decorator(f):
        # type: (Spec) -> Spec
        f.arguments = list(names)
        return f

    return decorator


def get_arguments(f):
    # type: (Spec) -> Arguments
    return getattr(f, "arguments", [])
