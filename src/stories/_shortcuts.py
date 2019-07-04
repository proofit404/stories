from typing import Callable, Type, Union

from ._mounted import ClassMountedStory
from ._types import ClassWithSpec, ContextContract, FailureProtocol


ContractIn = Union[ContextContract, Callable[[ContextContract], ContextContract]]


def contract_in(
    cls,  # type: Type[ClassWithSpec]
    *args  # type: ContextContract
):
    # type: (...) -> ContractIn
    def setter(contract):
        # type: (ContextContract) -> ContextContract
        for attrname in dir(cls):
            attribute = getattr(cls, attrname)
            if type(attribute) is ClassMountedStory:
                attribute.contract(contract)
        return contract

    if args:
        return setter(*args)
    else:
        return setter


FailuresIn = Union[FailureProtocol, Callable[[FailureProtocol], FailureProtocol]]


def failures_in(
    cls,  # type: Type[ClassWithSpec]
    *args  # type: FailureProtocol
):
    # type: (...) -> FailuresIn
    def setter(failures):
        # type: (FailureProtocol) -> FailureProtocol
        for attrname in dir(cls):
            attribute = getattr(cls, attrname)
            if type(attribute) is ClassMountedStory:
                attribute.failures(failures)
        return failures

    if args:
        return setter(*args)
    else:
        return setter
