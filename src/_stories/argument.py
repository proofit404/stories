# -*- coding: utf-8 -*-
from _stories.exceptions import StoryDefinitionError


def arguments(*names):
    if not names:
        raise StoryDefinitionError("Story arguments can not be an empty list")

    if any(name for name in names if not isinstance(name, str)):
        message = "Story arguments can only be defined with string type"
        raise StoryDefinitionError(message)

    def decorator(f):
        f.arguments = list(names)
        return f

    return decorator


def get_arguments(f):
    return getattr(f, "arguments", [])
