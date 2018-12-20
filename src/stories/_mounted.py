from ._collect import wrap_story
from ._context import Context
from ._contract import Contract, validate_arguments
from ._exec import function
from ._failures import make_protocol
from ._history import History
from ._repr import story_representation
from ._run import Call, Run


class ClassMountedStory(object):
    def __init__(self, cls, name, collected, failures):
        self.cls = cls
        self.obj = None
        self.cls_name = cls.__name__
        self.name = name
        self.collected = collected
        self.failures = failures

    def __repr__(self):
        return story_representation(
            is_story,
            self.cls_name + "." + self.name,
            self.cls,
            self.obj,
            self.collected,
        )


class MountedStory(object):
    def __init__(self, cls, obj, name, arguments, collected, protocol):
        self.cls = cls
        self.obj = obj
        self.cls_name = cls.__name__
        self.name = name
        self.arguments = arguments
        self.collected = collected  # TODO: Remove.
        self.protocol = protocol
        self.methods, self.failures = wrap_story(
            is_story, collected, cls.__name__, name, obj, protocol
        )

    def __call__(self, *args, **kwargs):
        history = History(self.cls_name, self.name)
        ctx = Context(validate_arguments(self.arguments, args, kwargs), history)
        contract = Contract()
        runner = Call(make_protocol(self.failures))
        return function.execute(runner, ctx, self.methods, contract)

    def run(self, *args, **kwargs):
        history = History(self.cls_name, self.name)
        ctx = Context(validate_arguments(self.arguments, args, kwargs), history)
        contract = Contract()
        runner = Run(make_protocol(self.failures), self.cls_name, self.name)
        return function.execute(runner, ctx, self.methods, contract)

    def __repr__(self):
        return story_representation(
            is_story,
            self.cls_name + "." + self.name,
            self.cls,
            self.obj,
            self.collected,
        )


def is_story(attribute):
    return type(attribute) in {ClassMountedStory, MountedStory}
