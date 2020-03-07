# -*- coding: utf-8 -*-
from _stories.context import make_context
from _stories.failures import make_run_protocol
from _stories.history import History
from _stories.marker import BeginningOfStory
from _stories.marker import EndOfStory
from _stories.run import Call
from _stories.run import Run


class ClassMountedStory(object):
    def __init__(self, cls, name, collected, contract, failures):
        self.cls = cls
        self.name = name
        self.collected = collected
        self.contract = contract
        self.failures = failures

    def __repr__(self):
        result = [self.cls.__name__ + "." + self.name]
        for name in self.collected:
            attr = getattr(self.cls, name, None)
            if type(attr) is ClassMountedStory:
                result.append("  " + attr.name)
                result.extend(["  " + line for line in repr(attr).splitlines()[1:]])
            else:
                defined = "" if attr else " ??"
                result.append("  " + name + defined)
        return "\n".join(result)


class MountedStory(object):
    def __init__(
        self, obj, cls_name, name, arguments, methods, contract, failures, executor
    ):
        self.obj = obj
        self.cls_name = cls_name
        self.name = name
        self.arguments = arguments
        self.methods = methods
        self.contract = contract
        self.failures = failures
        self.executor = executor

    def __call__(self, **kwargs):
        __tracebackhide__ = True
        history = History()
        ctx, ns, lines, bind = make_context(self.methods[0][1], kwargs, history)
        runner = Call()
        return self.executor(runner, ctx, ns, bind, history, self.methods)

    def run(self, **kwargs):
        __tracebackhide__ = True
        history = History()
        ctx, ns, lines, bind = make_context(self.methods[0][1], kwargs, history)
        run_protocol = make_run_protocol(self.failures, self.cls_name, self.name)
        runner = Run(run_protocol)
        return self.executor(runner, ctx, ns, bind, history, self.methods)

    def __repr__(self):
        result = []
        indent = 0
        for method, _contract, _protocol in self.methods:
            method_type = type(method)
            if method_type is BeginningOfStory:
                result.append("  " * indent + method.story_name)
                indent += 1
            elif method_type is EndOfStory:
                indent -= 1
            else:
                result.append("  " * indent + method.__name__)
        return "\n".join(result)
