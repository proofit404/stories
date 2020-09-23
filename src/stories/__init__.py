"""
stories
-------

This module implements Business Transaction DSL.

:copyright: (c) 2018-2020 Artem Malyshev.
:license: BSD, see LICENSE for more details.
"""
from _stories.argument import arguments
from _stories.returned import Failure
from _stories.returned import Next
from _stories.returned import Result
from _stories.returned import Success
from _stories.story import story


__all__ = ["story", "arguments", "Result", "Success", "Failure", "Next"]
