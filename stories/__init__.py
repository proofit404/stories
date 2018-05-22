"""
stories
-------

This module implements Business Transaction DSL.

:copyright: (c) 2018 by Artem Malyshev.
:license: BSD, see LICENSE for more details.
"""


from ._base import Failure, Result, Skip, Success, argument, story


__all__ = ["story", "argument", "Result", "Success", "Failure", "Skip"]
