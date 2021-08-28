from _stories.execute import _Executor
from _stories.step import _Step


class _StoryType(type):
    def __prepare__(class_name, bases):
        return {"I": _Step()}

    def __new__(cls, class_name, bases, namespace):
        steps = namespace.pop("I").steps
        if not bases:
            return type.__new__(cls, class_name, bases, namespace)
        namespace["__call__"] = _Executor(steps)
        return type.__new__(cls, class_name, bases, namespace)


class Story(metaclass=_StoryType):
    """Business process specification.

    Use sentences from business domain to express its steps.

    """
