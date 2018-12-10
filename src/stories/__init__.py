"""
stories
-------

This module implements Business Transaction DSL.

:copyright: (c) 2018 by Artem Malyshev.
:license: BSD, see LICENSE for more details.
"""

from ._argument import argument
from ._return import Failure, Result, Skip, Success
from ._story import Story as story


__all__ = ["story", "argument", "Result", "Success", "Failure", "Skip"]
