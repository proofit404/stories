from ._argument import get_arguments
from ._collect import collect_story
from ._failures import check_data_type
from ._mounted import ClassMountedStory, MountedStory
from ._wrap import wrap_story


class Story(object):
    def __init__(self, f):
        self.name = f.__name__
        self.arguments = get_arguments(f)
        self.collected = collect_story(f)
        self.failures(None)

    def __get__(self, obj, cls):
        if obj is None:
            return ClassMountedStory(cls, self.name, self.collected, self.failures)
        else:
            methods, failures = wrap_story(
                self.arguments,
                self.collected,
                cls.__name__,
                self.name,
                obj,
                self.__failures,
            )
            return MountedStory(
                obj, cls.__name__, self.name, self.arguments, methods, failures
            )

    def failures(self, failures):
        check_data_type(failures)
        self.__failures = failures
        return failures
