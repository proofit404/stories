"""
stories.exceptions
------------------

This module contains errors definitions user can handle.

:copyright: (c) 2018-2019 dry-python team.
:license: BSD, see LICENSE for more details.
"""

from ._types import FailureVariant


class StoryError(Exception):
    pass


class StoryDefinitionError(StoryError):
    pass


class FailureError(StoryError):
    def __init__(self, reason):
        # type: (FailureVariant) -> None
        self.__reason = reason
        super(FailureError, self).__init__()

    def __repr__(self):
        # type: () -> str
        reason = repr(self.__reason) if self.__reason else ""
        return "FailureError(" + reason + ")"


class FailureProtocolError(StoryError):
    pass


class ContextContractError(StoryError):
    pass


class MutationError(StoryError):
    pass
