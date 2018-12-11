from ._collect import wrap_story
from ._context import Context, validate_arguments
from ._contract import Contract
from ._exec import function
from ._history import History
from ._repr import story_representation
from ._run import Call, Run


class ClassMountedStory(object):
    def __init__(self, cls, name, collected, failures):
        self.cls = cls
        self.cls_name = cls.__name__
        self.name = name
        self.collected = collected
        self.failures = failures

    def __repr__(self):
        return story_representation(
            is_story, self.cls_name + "." + self.name, self.cls, None, self.collected
        )


class MountedStory(object):
    def __init__(self, cls, obj, name, arguments, collected, protocol):
        self.cls = cls
        self.obj = obj
        self.cls_name = cls.__name__
        self.name = name
        self.arguments = arguments
        self.collected = collected
        self.protocol = protocol

    def __call__(self, *args, **kwargs):
        runner = Call(self.protocol)
        history = History(self.cls_name, self.name)
        ctx = Context(validate_arguments(self.arguments, args, kwargs), history)
        methods = wrap_story(
            is_story,
            self.collected,
            self.obj,
            self.protocol,
            self.cls_name,
            self.name,
            ctx,
        )
        contract = Contract()
        return function.execute(runner, ctx, methods, contract, self.protocol)

    def run(self, *args, **kwargs):
        runner = Run(self.protocol, self.cls_name, self.name)
        history = History(self.cls_name, self.name)
        ctx = Context(validate_arguments(self.arguments, args, kwargs), history)
        methods = wrap_story(
            is_story,
            self.collected,
            self.obj,
            self.protocol,
            self.cls_name,
            self.name,
            ctx,
        )
        contract = Contract()
        return function.execute(runner, ctx, methods, contract, self.protocol)

    def __repr__(self):
        return story_representation(
            is_story,
            self.cls_name + "." + self.name,
            self.cls,
            self.obj,
            self.collected,
        )

    @property
    def failures(self):
        return self.protocol.failures


def is_story(attribute):
    return callable(attribute) and type(attribute) is MountedStory
