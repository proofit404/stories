# -*- coding: utf-8 -*-
from stories import Success


# Mixins.


class NormalMethod(object):
    def one(self, ctx):
        return Success()


class StringMethod(object):
    def one(self, ctx):
        ctx.foo = "1"
        ctx.bar = ["2"]
        return Success()


class WrongMethod(object):
    def one(self, ctx):
        ctx.foo = "<boom>"


class UnknownMethod(object):
    def one(self, ctx):
        ctx.spam = "0"


class ExceptionMethod(object):
    def one(self, ctx):
        raise Exception


class AliasMethod(object):
    def one(self, ctx):
        value = {"key": "1"}
        ctx.foo = value
        ctx.bar = value
        ctx.baz = value
        return Success()


# Next child mixins.


class NormalNextMethod(object):
    def two(self, ctx):
        return Success()


# Parent mixins.


class NormalParentMethod(object):
    def before(self, ctx):
        return Success()

    def after(self, ctx):
        return Success()


class StringParentMethod(object):
    def before(self, ctx):
        ctx.foo = "1"
        ctx.bar = ["2"]
        return Success()

    def after(self, ctx):
        return Success()


class ExceptionParentMethod(object):
    def before(self, ctx):
        raise Exception

    def after(self, ctx):
        return Success()


# Root mixins.


class NormalRootMethod(object):
    def start(self, ctx):
        return Success()

    def finish(self, ctx):
        return Success()


class StringRootMethod(object):
    def start(self, ctx):
        ctx.foo = "1"
        ctx.bar = ["2"]
        return Success()

    def finish(self, ctx):
        return Success()


class StringWideRootMethod(object):
    def start(self, ctx):
        ctx.foo = "1"
        ctx.bar = ["2"]
        ctx.baz = "1"
        return Success()

    def finish(self, ctx):
        return Success()


class ExceptionRootMethod(object):
    def start(self, ctx):
        raise Exception

    def finish(self, ctx):
        return Success()
