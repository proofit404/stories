# TODO:
#
# [ ]: Check incoming reasons type.
from enum import Enum, unique

from stories import Failure, StoryFactory


# Simple.


story = StoryFactory(failures=["foo", "bar", "baz"])


class SimpleWithList(object):
    @story
    def x(I):
        I.one

    def one(self, ctx):
        return Failure("foo")


@unique
class Errors(Enum):
    foo = 1
    bar = 2
    baz = 3


story = StoryFactory(failures=Errors)


class SimpleWithEnum(object):
    @story
    def x(I):
        I.one

    def one(self, ctx):
        return Failure(Errors.foo)
