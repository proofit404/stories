from examples.methods import *  # noqa: F403
from stories import arguments
from stories import Failure
from stories import Next
from stories import Result
from stories import story
from stories import Success


# Mixins.


class MixedCoroutineMethod(object):
    def a1s1(self, ctx):
        pass  # pragma: no cover

    def a1s2(self, ctx):
        pass  # pragma: no cover

    async def a1s3(self, ctx):
        pass  # pragma: no cover


class MixedFunctionMethod(object):
    async def a1s1(self, ctx):
        pass  # pragma: no cover

    async def a1s2(self, ctx):
        pass  # pragma: no cover

    def a1s3(self, ctx):
        pass  # pragma: no cover


class NormalMethod(object):
    async def a1s1(self, ctx):
        return Success()

    async def a1s2(self, ctx):
        return Success()

    async def a1s3(self, ctx):
        return Success()


class FailureMethod(object):
    async def a1s1(self, ctx):
        return Success()

    async def a1s2(self, ctx):
        return Failure()

    async def a1s3(self, ctx):
        pass  # pragma: no cover


class ResultMethod(object):
    async def a1s1(self, ctx):
        return Success()

    async def a1s2(self, ctx):
        return Result(-1)

    async def a1s3(self, ctx):
        pass  # pragma: no cover


class PassMethod(object):
    async def a1s1(self, ctx):
        pass

    async def a1s2(self, ctx):
        pass  # pragma: no cover

    async def a1s3(self, ctx):
        pass  # pragma: no cover


class DependencyMethod(object):
    async def a1s1(self, ctx):
        return Success()

    async def a1s2(self, ctx):
        ctx.a1v3 = self.f(ctx.a1v1, ctx.a1v2)
        return Success()

    async def a1s3(self, ctx):
        return Result(ctx.a1v3)


class FunctionMethod(object):
    def a1s1(self, ctx):
        pass  # pragma: no cover

    def a1s2(self, ctx):
        pass  # pragma: no cover

    def a1s3(self, ctx):
        pass  # pragma: no cover


# Parent mixins.


class NormalParentMethod(object):
    async def b1s1(self, ctx):
        return Success()

    async def b1s2(self, ctx):
        return Success()


class AssignParentMethod(object):
    async def b1s1(self, ctx):
        ctx.a1v1 = 2
        ctx.a1v2 = 4
        return Success()

    async def b1s2(self, ctx):
        pass  # pragma: no cover


class DependencyParentMethod(object):
    async def b1s1(self, ctx):
        ctx.a1v1 = self.f(ctx.b1v1)
        ctx.a1v2 = self.f(ctx.a1v1)
        return Success()

    async def b1s2(self, ctx):
        pass  # pragma: no cover


class FunctionParentMethod(object):
    def b1s1(self, ctx):
        pass  # pragma: no cover

    def b1s2(self, ctx):
        pass  # pragma: no cover


# Root mixins.


class NormalRootMethod(object):
    async def c1s1(self, ctx):
        return Success()

    async def c1s2(self, ctx):
        return Success()


class AssignRootMethod(object):
    async def c1s1(self, ctx):
        ctx.b1v1 = 3
        return Success()

    async def c1s2(self, ctx):
        pass  # pragma: no cover


class DependencyRootMethod(object):
    async def c1s1(self, ctx):
        ctx.b1v1 = self.f(ctx.c1v1)
        return Success()

    async def c1s2(self, ctx):
        pass  # pragma: no cover


# Story factories.


def define_coroutine_story():
    class Action(object):
        @story
        async def do(I):
            pass  # pragma: no cover
