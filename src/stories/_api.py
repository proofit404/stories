from ._collect import collect_story
from ._failures import make_protocol
from ._wrapper import StoryWrapper


class story(object):
    def __init__(self, f):
        self.name = f.__name__
        self.arguments = getattr(f, "arguments", [])
        self.collected = collect_story(f)
        self.protocol = make_protocol(None)

    def __get__(self, obj, cls):
        return StoryWrapper(
            cls, obj, self.name, self.arguments, self.collected, self.protocol
        )

    def failures(self, failures):
        # TODO: Allow to set failures from the global scope
        # (@Class.story.failures).
        self.protocol = make_protocol(failures)
        return failures


def argument(name):
    def decorator(f):
        if not hasattr(f, "arguments"):
            f.arguments = []
        f.arguments.insert(0, name)
        return f

    return decorator
