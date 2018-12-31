from ._collect import collect_story
from ._contract import make_contract
from ._failures import check_data_type
from ._mounted import ClassMountedStory, MountedStory


class Story(object):
    def __init__(self, f):
        self.name = f.__name__
        self.arguments = getattr(f, "arguments", [])
        self.collected = collect_story(f)
        self.contract = make_contract()
        self.failures(None)

    def __get__(self, obj, cls):
        if obj is None:
            return ClassMountedStory(cls, self.name, self.collected, self.failures)
        else:
            return MountedStory(
                cls,
                obj,
                self.name,
                self.arguments,
                self.collected,
                self.contract,
                self.__failures,
            )

    def failures(self, failures):
        check_data_type(failures)
        self.__failures = failures
        return failures
