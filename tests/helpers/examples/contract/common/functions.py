from stories import Success


# Mixins.


class NormalMethod(object):
    def a1s1(self, ctx):
        return Success()


class StringMethod(object):
    def a1s1(self, ctx):
        ctx.a1v1 = "1"
        ctx.a1v2 = ["2"]
        return Success()


class WrongMethod(object):
    def a1s1(self, ctx):
        ctx.a1v1 = "<boom>"


class UnknownMethod(object):
    def a1s1(self, ctx):
        ctx.spam = "0"


class ExceptionMethod(object):
    def a1s1(self, ctx):
        raise Exception


class AliasMethod(object):
    def a1s1(self, ctx):
        value = {"key": "1"}
        ctx.a1v1 = value
        ctx.a1v2 = value
        ctx.a1v3 = value
        return Success()


# Next child mixins.


class NormalNextMethod(object):
    def a2s1(self, ctx):
        return Success()


# Parent mixins.


class NormalParentMethod(object):
    def b1s1(self, ctx):
        return Success()

    def b1s2(self, ctx):
        return Success()


class StringParentMethod(object):
    def b1s1(self, ctx):
        ctx.a1v1 = "1"
        ctx.a1v2 = ["2"]
        return Success()

    def b1s2(self, ctx):
        return Success()


class ExceptionParentMethod(object):
    def b1s1(self, ctx):
        raise Exception

    def b1s2(self, ctx):
        return Success()


# Root mixins.


class NormalRootMethod(object):
    def c1s1(self, ctx):
        return Success()

    def c1s2(self, ctx):
        return Success()


class StringRootMethod(object):
    def c1s1(self, ctx):
        ctx.a1v1 = "1"
        ctx.a1v2 = ["2"]
        return Success()

    def c1s2(self, ctx):
        return Success()


class StringWideRootMethod(object):
    def c1s1(self, ctx):
        ctx.a1v1 = "1"
        ctx.a1v2 = ["2"]
        ctx.a1v3 = "1"
        return Success()

    def c1s2(self, ctx):
        return Success()


class ExceptionRootMethod(object):
    def c1s1(self, ctx):
        raise Exception

    def c1s2(self, ctx):
        return Success()
