"""
stories
-------

This module implements Business Transaction DSL.

:copyright: (c) 2018-2020 dry-python team.
:license: BSD, see LICENSE for more details.
"""
from _stories.argument import arguments
from _stories.returned import Failure
from _stories.returned import Result
from _stories.returned import Skip
from _stories.returned import Success
from _stories.story import Story as story


__all__ = ["story", "arguments", "Result", "Success", "Failure", "Skip"]
