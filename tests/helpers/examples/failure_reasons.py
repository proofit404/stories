# TODO:
#
# [ ] Substory can not use failures from the protocol superset of the
#     parent story.
#
# [ ] Protocol errors should be visible in the context representation.
#
# [ ] Expand parent and substory expand:
#
#     - Substory with empty result can not return failure if parent
#       story defines errors protocol.
#
#     - Story with empty result can not return failure if child story
#       defines errors protocol.


from enum import Enum

from stories import Failure, Success, story


# Mixins.


class StringMethod(object):
    def one(self, ctx):
        return Failure("foo")


class EnumMethod(object):
    def one(self, ctx):
        return Failure(self.Errors.foo)


class NormalMethod(object):
    def one(self, ctx):
        return Success()


class WrongMethod(object):
    def one(self, ctx):
        return Failure("'foo' is too big")


class NullMethod(object):
    def one(self, ctx):
        return Failure()


class ParentMethod(object):
    def before(self, ctx):
        return Success()

    def after(self, ctx):
        return Success()


class ChildWithNull(object):
    @story
    def x(I):
        I.one


class ParentWithNull(object):
    @story
    def a(I):
        I.before
        I.x
        I.after


class ChildWithList(object):
    @story
    def x(I):
        I.one

    errors = x.failures(["foo", "bar", "baz"])


class ParentWithList(object):
    @story
    def a(I):
        I.before
        I.x
        I.after

    a.failures(["foo", "bar", "baz"])


class WideParentWithList(object):
    @story
    def a(I):
        I.before
        I.x
        I.after

    errors = a.failures(["foo", "bar", "baz", "quiz"])


class ShrinkParentWithList(object):
    @story
    def a(I):
        I.before
        I.x
        I.after

    errors = a.failures(["foo", "quiz"])


class ChildWithEnum(object):
    @story
    def x(I):
        I.one

    @x.failures
    class Errors(Enum):
        foo = 1
        bar = 2
        baz = 3


class ParentWithEnum(object):
    @story
    def a(I):
        I.before
        I.x
        I.after

    @a.failures
    class Errors(Enum):
        foo = 1
        bar = 2
        baz = 3


class WideParentWithEnum(object):
    @story
    def a(I):
        I.before
        I.x
        I.after

    @a.failures
    class Errors(Enum):
        foo = 1
        bar = 2
        baz = 3
        quiz = 4


class ShrinkParentWithEnum(object):
    @story
    def a(I):
        I.before
        I.x
        I.after

    @a.failures
    class Errors(Enum):
        foo = 1
        quiz = 4
