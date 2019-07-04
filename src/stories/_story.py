from typing import Optional, Type, Union

from ._argument import get_arguments
from ._collect import collect_story
from ._failures import check_data_type
from ._mounted import ClassMountedStory, MountedStory
from ._types import ClassWithSpec, ContextContract, FailureProtocol, Spec
from ._wrap import wrap_story


class Story(object):
    def __init__(self, f):
        # type: (Spec) -> None
        self.name = f.__name__
        self.arguments = get_arguments(f)
        self.collected = collect_story(f)
        self.contract(None)
        self.failures(None)

    def __get__(
        self,
        obj,  # type: Optional[ClassWithSpec]
        cls,  # type: Type[ClassWithSpec]
    ):
        # type: (...) -> Union[ClassMountedStory, MountedStory]
        __tracebackhide__ = True
        if obj is None:
            return ClassMountedStory(
                cls, self.name, self.collected, self.contract, self.failures
            )
        else:
            methods, contract, failures = wrap_story(
                self.arguments,
                self.collected,
                cls.__name__,
                self.name,
                obj,
                self.__contract,
                self.__failures,
            )
            return MountedStory(
                obj,
                cls.__name__,
                self.name,
                self.arguments,
                methods,
                contract,
                failures,
            )

    def contract(self, contract):
        # type: (ContextContract) -> ContextContract
        # FIXME: Raise error on unsupported types.
        self.__contract = contract
        return contract

    def failures(self, failures):
        # type: (FailureProtocol) -> FailureProtocol
        check_data_type(failures)
        self.__failures = failures  # type: FailureProtocol
        return failures
