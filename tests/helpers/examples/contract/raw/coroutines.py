# -*- coding: utf-8 -*-
from examples.contract.raw import *  # noqa: F401, F403
from stories import Success


# Mixins.


class NormalMethod(object):
    async def one(self, ctx):
        return Success()


class StringMethod(object):
    async def one(self, ctx):
        return Success(foo="1", bar=["2"])


class WrongMethod(object):
    async def one(self, ctx):
        return Success(foo="<boom>", bar=["<boom>"])


class UnknownMethod(object):
    async def one(self, ctx):
        return Success(spam="0", quiz="1")


class ExceptionMethod(object):
    async def one(self, ctx):
        raise Exception


class AliasMethod(object):
    async def one(self, ctx):
        value = {"key": "1"}
        return Success(foo=value, bar=value, baz=value)


# Next child mixins.


class NormalNextMethod(object):
    async def two(self, ctx):
        return Success()


# Parent mixins.


class NormalParentMethod(object):
    async def before(self, ctx):
        return Success()

    async def after(self, ctx):
        return Success()


class StringParentMethod(object):
    async def before(self, ctx):
        return Success(foo="1", bar=["2"])

    async def after(self, ctx):
        return Success()


class ExceptionParentMethod(object):
    async def before(self, ctx):
        raise Exception

    async def after(self, ctx):
        return Success()


# Root mixins.


class NormalRootMethod(object):
    async def start(self, ctx):
        return Success()

    async def finish(self, ctx):
        return Success()


class StringRootMethod(object):
    async def start(self, ctx):
        return Success(foo="1", bar=["2"])

    async def finish(self, ctx):
        return Success()


class StringWideRootMethod(object):
    async def start(self, ctx):
        return Success(foo="1", bar=["2"], baz="1")

    async def finish(self, ctx):
        return Success()


class ExceptionRootMethod(object):
    async def start(self, ctx):
        raise Exception

    async def finish(self, ctx):
        return Success()
