"""
stories
-------

This module implements Business Transaction DSL.

:copyright: (c) 2018-2019 dry-python team.
:license: BSD, see LICENSE for more details.
"""

from _stories.argument import arguments
from _stories.returned import Failure, Result, Skip, Success
from _stories.story import Story as story


__all__ = ["story", "arguments", "Result", "Success", "Failure", "Skip"]
