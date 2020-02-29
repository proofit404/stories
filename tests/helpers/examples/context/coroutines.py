# -*- coding: utf-8 -*-
from examples.context import *  # noqa: F401, F403
from stories import Result
from stories import Success


# Mixins.


class PrivateMethod(object):
    async def one(self, ctx):
        return Result(ctx.__dict__)


class NormalMethod(object):
    async def one(self, ctx):
        return Success(foo=self.foo)


class AssignMethod(object):
    async def one(self, ctx):
        ctx.foo = 1


class DeleteMethod(object):
    async def one(self, ctx):
        del ctx.foo


class CompareMethod(object):
    async def one(self, ctx):
        if ctx:
            pass  # pragma: no cover


class DirMethod(object):
    async def one(self, ctx):
        return Result(dir(ctx))


# Parent mixins.


class NormalParentMethod(object):
    async def before(self, ctx):
        return Success()

    async def after(self, ctx):
        return Success()


class DirParentMethod(object):
    async def before(self, ctx):
        return Success()

    async def after(self, ctx):
        return Result(dir(ctx))
