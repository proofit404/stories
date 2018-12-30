from ._context import Context
from ._contract import validate_arguments
from ._exec import function
from ._failures import make_run_protocol
from ._history import History
from ._repr import story_representation
from ._run import Call, Run
from ._wrap import wrap_story


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
    def __init__(self, cls, obj, name, arguments, collected, contract, protocol):
        self.cls = cls
        self.obj = obj
        self.cls_name = cls_name = cls.__name__
        self.name = name
        self.arguments = arguments
        self.collected = collected  # TODO: Remove.
        self.contract = contract
        self.methods, self.failures = wrap_story(
            is_story, arguments, collected, cls_name, name, obj, contract, protocol
        )

    def __call__(self, *args, **kwargs):
        history = History()
        ctx = Context(
            validate_arguments(self.arguments, args, kwargs), history, self.contract
        )
        runner = Call()
        return function.execute(runner, ctx, self.methods)

    def run(self, *args, **kwargs):
        history = History()
        ctx = Context(
            validate_arguments(self.arguments, args, kwargs), history, self.contract
        )
        run_protocol = make_run_protocol(self.failures, self.cls_name, self.name)
        runner = Run(run_protocol)
        return function.execute(runner, ctx, self.methods)

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
