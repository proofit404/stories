from ._collect import wrap_story
from ._context import Context, validate_arguments
from ._contract import Contract
from ._exec import function
from ._failures import Protocol
from ._history import History
from ._repr import story_representation
from ._run import Call, Run


class StoryWrapper(object):
    def __init__(self, cls, obj, name, arguments, collected, failures):
        self.cls = cls
        self.obj = obj
        self.cls_name = cls.__name__
        self.name = name
        self.arguments = arguments
        self.collected = collected
        self.failures = failures

    def __call__(self, *args, **kwargs):
        runner = Call()
        history = History(self.cls_name, self.name)
        ctx = Context(validate_arguments(self.arguments, args, kwargs), history)
        methods = wrap_story(is_story, self.collected, self.obj, ctx)
        contract = Contract()
        protocol = Protocol(self.cls, self.failures)
        return function.execute(runner, ctx, methods, contract, protocol)

    def run(self, *args, **kwargs):
        runner = Run()
        history = History(self.cls_name, self.name)
        ctx = Context(validate_arguments(self.arguments, args, kwargs), history)
        methods = wrap_story(is_story, self.collected, self.obj, ctx)
        contract = Contract()
        protocol = Protocol(self.cls, self.failures)
        return function.execute(runner, ctx, methods, contract, protocol)

    def __repr__(self):
        return story_representation(
            is_story,
            self.cls_name + "." + self.name,
            self.cls,
            self.obj,
            self.collected,
        )


def is_story(attribute):
    return callable(attribute) and type(attribute) is StoryWrapper
