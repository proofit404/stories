"""
stories
-------

This module implements Business Transaction DSL.

:copyright: (c) 2018 by Artem Malyshev.
:license: BSD, see LICENSE for more details.
"""

from ._api import argument, story
from ._return import Failure, Result, Skip, Success


__all__ = ["story", "argument", "Result", "Success", "Failure", "Skip"]
