# -*- coding: utf-8 -*-
from _stories.compat import iscoroutinefunction
from _stories.exceptions import StoryDefinitionError
from _stories.execute import function

try:
    from _stories.execute import coroutine
except SyntaxError:
    pass


def get_executor(method, previous, cls_name, story_name):
    if iscoroutinefunction(method):
        executor = coroutine.execute
        other_kind = "function"
    else:
        executor = function.execute
        other_kind = "coroutine"

    if previous is not executor and previous is not None:
        message = mixed_method_template.format(
            other_kind=other_kind,
            cls=cls_name,
            method=method.__name__,
            story_name=story_name,
        )
        raise StoryDefinitionError(message)
    return executor


# Messages.


mixed_method_template = """
Coroutines and functions can not be used together in story definition.

This method should be a {other_kind}: {cls}.{method}

Story method: {cls}.{story_name}
""".strip()
