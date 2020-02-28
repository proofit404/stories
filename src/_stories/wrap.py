# -*- coding: utf-8 -*-
from _stories.contract import combine_contract
from _stories.contract import make_contract
from _stories.contract import maybe_extend_downstream_argsets
from _stories.exceptions import StoryDefinitionError
from _stories.execute import get_executor
from _stories.failures import combine_failures
from _stories.failures import make_exec_protocol
from _stories.failures import maybe_disable_null_protocol
from _stories.marker import BeginningOfStory
from _stories.marker import EndOfStory
from _stories.mounted import MountedStory


def wrap_story(arguments, collected, cls_name, story_name, obj, spec, failures):
    __tracebackhide__ = True

    executor = None
    contract = make_contract(cls_name, story_name, arguments, spec)
    protocol = make_exec_protocol(failures)

    methods = [(BeginningOfStory(cls_name, story_name), contract, protocol)]

    for name in collected:

        attr = getattr(obj, name)

        if type(attr) is not MountedStory:
            executor = get_executor(attr, executor, cls_name, story_name)
            methods.append((attr, contract, protocol))
            continue

        if executor is not None and executor is not attr.executor:
            message = mixed_composition_template.format(
                kind=executor.__module__.rsplit(".", 1)[-1],
                cls=cls_name,
                method=story_name,
                other_kind=attr.executor.__module__.rsplit(".", 1)[-1],
                other_cls=attr.cls_name,
                other_method=attr.name,
            )
            raise StoryDefinitionError(message)
        elif executor is None:
            executor = attr.executor

        combine_contract(contract, attr.contract)

        failures = combine_failures(
            failures, cls_name, story_name, attr.failures, attr.cls_name, attr.name
        )

        # FIXME: Is there a way to avoid this modification?
        attr.methods[0][0].set_parent(name, attr.obj is obj)

        methods.extend(attr.methods)

    methods.append((EndOfStory(), contract, protocol))

    maybe_extend_downstream_argsets(methods, contract)

    methods = maybe_disable_null_protocol(methods, failures)

    return methods, contract, failures, executor


# Messages.


mixed_composition_template = """
Coroutine and function stories can not be injected into each other.

Story {kind} method: {cls}.{method}

Substory {other_kind} method: {other_cls}.{other_method}
""".strip()
