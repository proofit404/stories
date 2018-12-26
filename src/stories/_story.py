from ._collect import collect_story
from ._contract import make_contract
from ._failures import make_protocol
from ._mounted import ClassMountedStory, MountedStory


class Story(object):
    def __init__(self, f):
        self.name = f.__name__
        self.arguments = getattr(f, "arguments", [])
        self.collected = collect_story(f)
        self.contract = make_contract()
        self.protocol = make_protocol(None)

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
                self.protocol,
            )

    def failures(self, failures):
        self.protocol = make_protocol(failures)
        return failures
