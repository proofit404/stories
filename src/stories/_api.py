from ._collect import collect_story
from ._failures import make_protocol
from ._wrapper import StoryWrapper


class story(object):
    failures = None

    def __init__(self, f):
        self.name = f.__name__
        self.arguments = getattr(f, "arguments", [])
        self.collected = collect_story(f)
        self.protocol = make_protocol(self.failures)

    def __get__(self, obj, cls):
        return StoryWrapper(
            cls, obj, self.name, self.arguments, self.collected, self.protocol
        )


def argument(name):
    def decorator(f):
        if not hasattr(f, "arguments"):
            f.arguments = []
        f.arguments.insert(0, name)
        return f

    return decorator
