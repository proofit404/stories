from _stories.execute import _get_executor
from _stories.step import _Step


class _StoryType(type):
    def __prepare__(class_name, bases):
        return {"I": _Step()}

    def __new__(cls, class_name, bases, namespace):
        if not bases:
            return type.__new__(cls, class_name, bases, namespace)
        del namespace["I"]
        namespace["__call__"] = _get_executor(
            [v for v in namespace.values() if callable(v)][0]
        )
        return type.__new__(cls, class_name, bases, namespace)


class Story(metaclass=_StoryType):
    """Business process specification.

    Use sentences from business domain to express its steps.

    """
