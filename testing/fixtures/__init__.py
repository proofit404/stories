from typing import Protocol

from fixtures import asynchronous
from fixtures import synchronous


class S(Protocol):
    actor_class: type[object]
    initiate: object
    story_class: type[object]

    @staticmethod
    def run(story: object, state: object) -> None:
        ...

    @staticmethod
    def normal_method(self: object, state: object) -> None:
        ...

    @staticmethod
    def assign_method(attribute: str, value: object) -> object:
        ...

    @staticmethod
    def assert_method(attribute: str, value: object) -> object:
        ...

    @staticmethod
    def append_method(attribute: str, value: object) -> object:
        ...

    @staticmethod
    def error_method(message: str) -> object:
        ...

    StepError: type[Exception]
