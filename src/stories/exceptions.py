# -*- coding: utf-8 -*-
"""
stories.exceptions
------------------

This module contains errors definitions user can handle.

:copyright: (c) 2018-2020 dry-python team.
:license: BSD, see LICENSE for more details.
"""
from _stories.exceptions import ContextContractError
from _stories.exceptions import FailureError
from _stories.exceptions import FailureProtocolError
from _stories.exceptions import MutationError
from _stories.exceptions import StoryDefinitionError
from _stories.exceptions import StoryError


__all__ = [
    "ContextContractError",
    "FailureError",
    "FailureProtocolError",
    "MutationError",
    "StoryDefinitionError",
    "StoryError",
]
