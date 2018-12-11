from enum import Enum

from stories import Failure, story
from stories.shortcuts import failures_in


class SimpleWithList(object):
    @story
    def x(I):
        I.y

    @story
    def y(I):
        I.one

    def one(self, ctx):
        return Failure("foo")


failures_in(SimpleWithList)(["foo", "bar", "baz"])


class SimpleWithEnum(object):
    @story
    def x(I):
        I.y

    @story
    def y(I):
        I.one

    def one(self, ctx):
        return Failure(Errors.foo)


@failures_in(SimpleWithEnum)
class Errors(Enum):
    foo = 1
    bar = 2
    baz = 3
