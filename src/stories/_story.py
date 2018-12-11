from ._collect import collect_story
from ._failures import make_protocol
from ._mounted import MountedStory


class Story(object):
    def __init__(self, f):
        self.name = f.__name__
        self.arguments = getattr(f, "arguments", [])
        self.collected = collect_story(f)
        self.protocol = make_protocol(None)

    def __get__(self, obj, cls):
        if obj is None:
            # FIXME: Test we can set failures from global namespace.
            #
            # @ClassName.story_method.failures
            # class Errors(Enum):
            #     foo = 1
            #     bar = 2
            #
            # ClassName.story_method.failures(["foo", "bar"])
            return self
        else:
            return MountedStory(
                cls, obj, self.name, self.arguments, self.collected, self.protocol
            )

    def failures(self, failures):
        self.protocol = make_protocol(failures)
        return failures
