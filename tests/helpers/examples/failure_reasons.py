# TODO:
#
# [ ]: Check incoming reasons type in the StoryFactory.
#
# [ ]: Story and substory protocol mismatch.
from enum import Enum, unique

from stories import Failure, StoryFactory


class Common(object):

    # Wrong reason.

    def two(self, ctx):
        return Failure("'foo' is too big")

    # Null reason.

    def three(self, ctx):
        return Failure()


# Simple.


story = StoryFactory(failures=["foo", "bar", "baz"])


class SimpleWithList(Common):
    @story
    def x(I):
        I.one

    def one(self, ctx):
        return Failure("foo")

    @story
    def y(I):
        I.two

    @story
    def z(I):
        I.three


@unique
class Errors(Enum):
    foo = 1
    bar = 2
    baz = 3


story = StoryFactory(failures=Errors)


class SimpleWithEnum(Common):
    @story
    def x(I):
        I.one

    def one(self, ctx):
        return Failure(Errors.foo)

    @story
    def y(I):
        I.two

    @story
    def z(I):
        I.three
