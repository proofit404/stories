"""
stories
-------

This module implements Business Transaction DSL.

:copyright: (c) 2018-2019 dry-python team.
:license: BSD, see LICENSE for more details.
"""

from ._argument import arguments
from ._return import Failure, Result, Skip, Success
from ._story import Story as story


__all__ = ["story", "arguments", "Result", "Success", "Failure", "Skip"]
