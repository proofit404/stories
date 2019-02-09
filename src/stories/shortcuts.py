"""
stories.shortcuts
-----------------

This module contains convenient functions to reduce boilerplate code.

:copyright: (c) 2018-2019 dry-python team.
:license: BSD, see LICENSE for more details.
"""

from ._mounted import ClassMountedStory


def failures_in(cls, *args):
    def setter(failures):
        for attrname in dir(cls):
            attribute = getattr(cls, attrname)
            if type(attribute) is ClassMountedStory:
                attribute.failures(failures)
        return failures

    if args:
        return setter(*args)
    else:
        return setter
