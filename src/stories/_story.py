import inspect
from ._argument import get_arguments
from ._collect import collect_story
from ._failures import check_data_type
from ._mounted import ClassMountedStory, MountedStory, AsyncMountedStory
from ._wrap import wrap_story


class Story(object):
    def __init__(self, f):
        self.name = f.__name__
        self.arguments = get_arguments(f)
        self.collected = collect_story(f)
        self.contract(None)
        self.failures(None)

    def __get__(self, obj, cls):
        if obj is None:
            return ClassMountedStory(
                cls, self.name, self.collected, self.contract, self.failures
            )
        else:
            methods, contract, failures = wrap_story(
                self.arguments,
                self.collected,
                cls.__name__,
                self.name,
                obj,
                self.__contract,
                self.__failures,
            )
            if any(inspect.iscoroutinefunction(item[0]) for item in methods):
                return AsyncMountedStory(
                    obj, cls.__name__, self.name, self.arguments, methods, specs, failures
                )
            return MountedStory(
                obj,
                cls.__name__,
                self.name,
                self.arguments,
                methods,
                contract,
                failures,
            )

    def contract(self, contract):
        # FIXME: Raise error on unsupported types.
        self.__contract = contract
        return contract

    def failures(self, failures):
        check_data_type(failures)
        self.__failures = failures
        return failures
