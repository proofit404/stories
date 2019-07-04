from ..exceptions import StoryDefinitionError
from . import function, coroutine

try:
    from inspect import iscoroutinefunction
except ImportError:
    iscoroutinefunction = lambda x: False


def get_executor(method, previous, cls_name, story_name):
    if iscoroutinefunction(method):
        executor = coroutine.execute
    else:
        executor = function.execute

    if previous is not None and previous is not executor:
        message = mixed_method_template.format(
            cls=cls_name, method=method.__name__, story_name=story_name
        )
        raise StoryDefinitionError(message)
    return executor


mixed_method_template = """
{cls}.{method} is a function but coroutine was expected.

Story method: {cls}.{story_name}

You can not use function and coroutine methods together.
""".strip()