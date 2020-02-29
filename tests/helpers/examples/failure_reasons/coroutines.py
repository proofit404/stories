# -*- coding: utf-8 -*-
from enum import Enum

from examples.failure_reasons import *  # noqa: F401, F403
from stories import Failure
from stories import Success


# Mixins.


class StringMethod(object):
    async def one(self, ctx):
        return Failure("foo")

    async def two(self, ctx):
        return Failure("spam")


class EnumMethod(object):
    async def one(self, ctx):
        Errors = Enum("Errors", "foo,bar,baz")
        return Failure(Errors.foo)

    async def two(self, ctx):
        Errors = Enum("Errors", "spam,ham,eggs")
        return Failure(Errors.spam)


class NormalMethod(object):
    async def one(self, ctx):
        return Success()

    async def two(self, ctx):
        return Success()


class WrongMethod(object):
    async def one(self, ctx):
        return Failure("'foo' is too big")

    async def two(self, ctx):
        return Failure("'foo' is too big")


class NullMethod(object):
    async def one(self, ctx):
        return Failure()

    async def two(self, ctx):
        return Failure()


# Parent mixins.


class StringParentMethod(object):
    async def before(self, ctx):
        return Failure("foo")

    async def after(self, ctx):
        return Success()


class EnumParentMethod(object):
    async def before(self, ctx):
        Errors = Enum("Errors", "foo,bar,baz")
        return Failure(Errors.foo)

    async def after(self, ctx):
        return Success()


class NormalParentMethod(object):
    async def before(self, ctx):
        return Success()

    async def after(self, ctx):
        return Success()


class NullParentMethod(object):
    async def before(self, ctx):
        return Failure()

    async def after(self, ctx):
        return Success()
