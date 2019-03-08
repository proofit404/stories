from enum import Enum

from stories import Failure, Success, story


# Mixins.


class StringMethod(object):
    def one(self, ctx):
        return Failure("foo")

    def two(self, ctx):
        return Failure("spam")


class EnumMethod(object):
    def one(self, ctx):
        Errors = Enum("Errors", "foo,bar,baz")
        return Failure(Errors.foo)

    def two(self, ctx):
        Errors = Enum("Errors", "spam,ham,eggs")
        return Failure(Errors.spam)


class NormalMethod(object):
    def one(self, ctx):
        return Success()

    def two(self, ctx):
        return Success()


class WrongMethod(object):
    def one(self, ctx):
        return Failure("'foo' is too big")

    def two(self, ctx):
        return Failure("'foo' is too big")


class NullMethod(object):
    def one(self, ctx):
        return Failure()

    def two(self, ctx):
        return Failure()


# Parent mixins.


class StringParentMethod(object):
    def before(self, ctx):
        return Failure("foo")

    def after(self, ctx):
        return Success()


class EnumParentMethod(object):
    def before(self, ctx):
        Errors = Enum("Errors", "foo,bar,baz")
        return Failure(Errors.foo)

    def after(self, ctx):
        return Success()


class NormalParentMethod(object):
    def before(self, ctx):
        return Success()

    def after(self, ctx):
        return Success()


class NullParentMethod(object):
    def before(self, ctx):
        return Failure()

    def after(self, ctx):
        return Success()


# Base classes.


class ChildWithNull(object):
    @story
    def x(I):
        I.one


class NextChildWithNull(object):
    @story
    def y(I):
        I.two


class ParentWithNull(object):
    @story
    def a(I):
        I.before
        I.x
        I.after


class SequenceParentWithNull(object):
    @story
    def a(I):
        I.before
        I.x
        I.y
        I.after


class ChildWithList(object):
    @story
    def x(I):
        I.one


ChildWithList.x.failures(["foo", "bar", "baz"])


class NextChildWithList(object):
    @story
    def y(I):
        I.two


NextChildWithList.y.failures(["spam", "ham", "eggs"])


class ParentWithList(object):
    @story
    def a(I):
        I.before
        I.x
        I.after


ParentWithList.a.failures(["foo", "bar", "baz"])


class WideParentWithList(object):
    @story
    def a(I):
        I.before
        I.x
        I.after


WideParentWithList.a.failures(["foo", "bar", "baz", "quiz"])


class ShrinkParentWithList(object):
    @story
    def a(I):
        I.before
        I.x
        I.after


ShrinkParentWithList.a.failures(["foo", "quiz"])


class ChildWithEnum(object):
    @story
    def x(I):
        I.one

    @x.failures
    class Errors(Enum):
        foo = 1
        bar = 2
        baz = 3


class NextChildWithEnum(object):
    @story
    def y(I):
        I.two

    @y.failures
    class Errors(Enum):
        spam = 1
        ham = 2
        eggs = 3


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
