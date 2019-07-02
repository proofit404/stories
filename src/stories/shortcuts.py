"""
stories.shortcuts
-----------------

This module contains convenient functions to reduce boilerplate code.

:copyright: (c) 2018-2019 dry-python team.
:license: BSD, see LICENSE for more details.
"""

from typing import Callable, Type, Union

from ._mounted import ClassMountedStory
from ._types import ClassWithSpec, ContextContract, FailureProtocol


def contract_in(
    cls,  # type: Type[ClassWithSpec]
    *args  # type: ContextContract
):
    # type: (...) -> Union[ContextContract, Callable[[ContextContract], ContextContract]]
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


def failures_in(
    cls,  # type: Type[ClassWithSpec]
    *args  # type: FailureProtocol
):
    # type: (...) -> Union[FailureProtocol, Callable[[FailureProtocol], FailureProtocol]]
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
