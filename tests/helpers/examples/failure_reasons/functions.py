# -*- coding: utf-8 -*-
from enum import Enum

from examples.failure_reasons import *  # noqa: F401, F403
from stories import Failure
from stories import Success


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
