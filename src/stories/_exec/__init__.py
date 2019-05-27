from ..exceptions import StoryDefinitionError
from . import function, coroutine

try:
    from inspect import iscoroutinefunction
except SyntaxError:
    iscoroutinefunction = lambda x: False


def get_executor(method, previous, cls_name):
    if iscoroutinefunction(method):
        executor = coroutine.execute
    else:
        executor = function.execute

    if previous is not None and previous is not executor:
        message = mixed_method_template.format(
            cls=cls_name, method=method.__name__
        )
        raise StoryDefinitionError(message)
    return executor


mixed_method_template = """
Class {cls} contains mixed method {method}'
""".strip()