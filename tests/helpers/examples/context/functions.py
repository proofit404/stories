# -*- coding: utf-8 -*-
from examples.context import *  # noqa: F401, F403
from stories import Result
from stories import Success


# Mixins.


class PrivateMethod(object):
    def one(self, ctx):
        return Result(ctx.__dict__)


class NormalMethod(object):
    def one(self, ctx):
        ctx.foo = self.foo
        return Success()


class DeleteMethod(object):
    def one(self, ctx):
        del ctx.foo


class CompareMethod(object):
    def one(self, ctx):
        if ctx:
            pass  # pragma: no cover


class DirMethod(object):
    def one(self, ctx):
        return Result(dir(ctx))


# Parent mixins.


class NormalParentMethod(object):
    def before(self, ctx):
        return Success()

    def after(self, ctx):
        return Success()


class DirParentMethod(object):
    def before(self, ctx):
        return Success()

    def after(self, ctx):
        return Result(dir(ctx))
