from typing import Callable, List, Tuple, Union

from ._contract import (
    ExecContract,
    combine_contract,
    make_contract,
    maybe_extend_downstream_argsets,
)
from ._failures import (
    ExecProtocol,
    combine_failures,
    make_exec_protocol,
    maybe_disable_null_protocol,
)
from ._marker import BeginningOfStory, EndOfStory
from ._mounted import MountedStory
from ._types import (
    Arguments,
    ClassWithSpec,
    Collected,
    ContextContract,
    FailureProtocol,
)


Method = Union[BeginningOfStory, EndOfStory, Callable]
Methods = List[Tuple[Method, ExecContract, ExecProtocol]]
Wrapped = Tuple[Methods, ExecContract, FailureProtocol]


def wrap_story(
    arguments,  # type: Arguments
    collected,  # type: Collected
    cls_name,  # type: str
    story_name,  # type: str
    obj,  # type: ClassWithSpec
    spec,  # type: ContextContract
    failures,  # type: FailureProtocol
):
    # type: (...) -> Wrapped
    __tracebackhide__ = True

    contract = make_contract(cls_name, story_name, arguments, spec)
    protocol = make_exec_protocol(failures)

    methods = [(BeginningOfStory(cls_name, story_name), contract, protocol)]

    for name in collected:

        attr = getattr(obj, name)

        if type(attr) is not MountedStory:
            methods.append((attr, contract, protocol))
            continue

        combine_contract(contract, attr.contract)

        failures = combine_failures(
            failures, cls_name, story_name, attr.failures, attr.cls_name, attr.name
        )

        # FIXME: Is there a way to avoid this modification?
        attr.methods[0][0].set_parent(name, attr.obj is obj)

        methods.extend(attr.methods)

    methods.append((EndOfStory(is_empty=not collected), contract, protocol))

    maybe_extend_downstream_argsets(methods, contract)

    methods = maybe_disable_null_protocol(methods, failures)

    return methods, contract, failures
