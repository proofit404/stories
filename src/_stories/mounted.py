# -*- coding: utf-8 -*-
from _stories.argument import get_arguments
from _stories.calls import CallSuperStory
from _stories.context import make_context
from _stories.contract import combine_contract
from _stories.contract import make_contract
from _stories.contract import maybe_extend_downstream_argsets
from _stories.exceptions import StoryDefinitionError
from _stories.execute import get_executor
from _stories.failures import combine_failures
from _stories.failures import make_exec_protocol
from _stories.failures import make_run_protocol
from _stories.failures import maybe_disable_null_protocol
from _stories.history import History
from _stories.marker import BeginningOfStory
from _stories.marker import EndOfStory
from _stories.run import Call
from _stories.run import Run


class ClassMountedStory(object):
    def __init__(self, cls, story_method, name, collected, contract, failures):
        self.cls = cls
        self.story_method = story_method
        self.name = name
        self.collected = collected
        self.contract = contract
        self.failures = failures

    @property
    def arguments(self):
        return get_arguments(self.story_method)

    @property
    def cls_name(self):
        return self.cls.__name__

    def wrap_story(self, obj, spec, failures):
        __tracebackhide__ = True

        executor = None
        contract = make_contract(self.cls_name, self.name, self.arguments, spec)
        protocol = make_exec_protocol(failures)

        methods = [(BeginningOfStory(self.cls_name, self.name), contract, protocol)]

        for call in self.collected:
            name = call.name
            attr = call.bind_to_object(obj)

            if type(attr) is not MountedStory:
                executor = get_executor(attr, executor, self.cls_name, self.name)
                methods.append((attr, contract, protocol))
                continue

            if executor is not None and executor is not attr.executor:
                message = mixed_composition_template.format(
                    kind=executor.__module__.rsplit(".", 1)[-1],
                    cls=self.cls_name,
                    method=self.name,
                    other_kind=attr.executor.__module__.rsplit(".", 1)[-1],
                    other_cls=attr.cls_name,
                    other_method=attr.name,
                )
                raise StoryDefinitionError(message)
            elif executor is None:
                executor = attr.executor

            combine_contract(contract, attr.contract)

            failures = combine_failures(
                failures,
                self.cls_name,
                self.name,
                attr.failures,
                attr.cls_name,
                attr.name,
            )

            # FIXME: Is there a way to avoid this modification?
            attr.methods[0][0].set_parent(
                name,
                attr.obj is obj,
                call.base_class.__name__ if call.base_class else None,
            )

            methods.extend(attr.methods)

        methods.append((EndOfStory(), contract, protocol))

        maybe_extend_downstream_argsets(methods, contract)

        methods = maybe_disable_null_protocol(methods, failures)

        return methods, contract, failures, executor

    def to_mounted_story(self, obj, contract=None, failures=None):
        methods, contract, failures, executor = self.wrap_story(obj, contract, failures)

        return MountedStory(
            obj,
            self.cls_name,
            self.name,
            self.arguments,
            methods,
            contract,
            failures,
            executor,
        )

    def __repr__(self):
        result = [self.cls.__name__ + "." + self.name]
        for call in self.collected:
            name = call.name
            attr = getattr(call.base_class or self.cls, name, None)
            if type(attr) is ClassMountedStory:
                if call.base_class is None:
                    result.append("  " + attr.name)
                else:
                    result.append(
                        "  "
                        + attr.name
                        + " (super story from {})".format(call.base_class.__name__)
                    )
                result.extend(["  " + line for line in repr(attr).splitlines()[1:]])
            else:
                defined = "" if attr else " ??"
                result.append("  " + name + defined)
        return "\n".join(result)

    def __call__(self, I):
        bases = self.cls.__bases__

        if self.name not in self.cls.__dict__:
            if len(bases) > 1:
                raise StoryDefinitionError(
                    multiple_inheritance_not_supported_template.format(
                        name=self.name, cls=self.cls_name
                    )
                )
            # Method is inherited but not overridden
            for base in self.cls.mro():
                if self.name in base.__dict__:
                    bases = base.__bases__
                    break

        for base in bases:
            if hasattr(base, self.name):
                I.__append_to_calls__(CallSuperStory(self.name, base))


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


# Messages.


mixed_composition_template = """
Coroutine and function stories can not be injected into each other.

Story {kind} method: {cls}.{method}

Substory {other_kind} method: {other_cls}.{other_method}
""".strip()

multiple_inheritance_not_supported_template = """
Multiple inheritance not supported when method {name} not overridden in {cls}
""".strip()
