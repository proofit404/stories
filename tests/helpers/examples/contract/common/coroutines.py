from stories import Success


# Mixins.


class NormalMethod(object):
    async def a1s1(self, ctx):
        return Success()


class StringMethod(object):
    async def a1s1(self, ctx):
        ctx.a1v1 = "1"
        ctx.a1v2 = ["2"]
        return Success()


class WrongMethod(object):
    async def a1s1(self, ctx):
        ctx.a1v1 = "<boom>"


class UnknownMethod(object):
    async def a1s1(self, ctx):
        ctx.spam = "0"


class ExceptionMethod(object):
    async def a1s1(self, ctx):
        raise Exception


class AliasMethod(object):
    async def a1s1(self, ctx):
        value = {"key": "1"}
        ctx.a1v1 = value
        ctx.a1v2 = value
        ctx.a1v3 = value
        return Success()


# Next child mixins.


class NormalNextMethod(object):
    async def a2s1(self, ctx):
        return Success()


# Parent mixins.


class NormalParentMethod(object):
    async def b1s1(self, ctx):
        return Success()

    async def b1s2(self, ctx):
        return Success()


class StringParentMethod(object):
    async def b1s1(self, ctx):
        ctx.a1v1 = "1"
        ctx.a1v2 = ["2"]
        return Success()

    async def b1s2(self, ctx):
        return Success()


class ExceptionParentMethod(object):
    async def b1s1(self, ctx):
        raise Exception

    async def b1s2(self, ctx):
        return Success()


# Root mixins.


class NormalRootMethod(object):
    async def c1s1(self, ctx):
        return Success()

    async def c1s2(self, ctx):
        return Success()


class StringRootMethod(object):
    async def c1s1(self, ctx):
        ctx.a1v1 = "1"
        ctx.a1v2 = ["2"]
        return Success()

    async def c1s2(self, ctx):
        return Success()


class StringWideRootMethod(object):
    async def c1s1(self, ctx):
        ctx.a1v1 = "1"
        ctx.a1v2 = ["2"]
        ctx.a1v3 = "1"
        return Success()

    async def c1s2(self, ctx):
        return Success()


class ExceptionRootMethod(object):
    async def c1s1(self, ctx):
        raise Exception

    async def c1s2(self, ctx):
        return Success()
