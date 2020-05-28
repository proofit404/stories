from examples.methods import *  # noqa: F403
from stories import arguments
from stories import Failure
from stories import Next
from stories import Result
from stories import story
from stories import Success


# Mixins.


class NormalMethod(object):
    def a1s1(self, ctx):
        return Success()

    def a1s2(self, ctx):
        return Success()

    def a1s3(self, ctx):
        return Success()


class FailureMethod(object):
    def a1s1(self, ctx):
        return Success()

    def a1s2(self, ctx):
        return Failure()

    def a1s3(self, ctx):
        pass  # pragma: no cover


class ResultMethod(object):
    def a1s1(self, ctx):
        return Success()

    def a1s2(self, ctx):
        return Result(-1)

    def a1s3(self, ctx):
        pass  # pragma: no cover


class PassMethod(object):
    def a1s1(self, ctx):
        pass

    def a1s2(self, ctx):
        pass  # pragma: no cover

    def a1s3(self, ctx):
        pass  # pragma: no cover


class DependencyMethod(object):
    def a1s1(self, ctx):
        return Success()

    def a1s2(self, ctx):
        ctx.a1v3 = self.f(ctx.a1v1, ctx.a1v2)
        return Success()

    def a1s3(self, ctx):
        return Result(ctx.a1v3)


# Parent mixins.


class NormalParentMethod(object):
    def b1s1(self, ctx):
        return Success()

    def b1s2(self, ctx):
        return Success()


class AssignParentMethod(object):
    def b1s1(self, ctx):
        ctx.a1v1 = 2
        ctx.a1v2 = 4
        return Success()

    def b1s2(self, ctx):
        pass  # pragma: no cover


class DependencyParentMethod(object):
    def b1s1(self, ctx):
        ctx.a1v1 = self.f(ctx.b1v1)
        ctx.a1v2 = self.f(ctx.a1v1)
        return Success()

    def b1s2(self, ctx):
        pass  # pragma: no cover


# Root mixins.


class NormalRootMethod(object):
    def c1s1(self, ctx):
        return Success()

    def c1s2(self, ctx):
        return Success()


class AssignRootMethod(object):
    def c1s1(self, ctx):
        ctx.b1v1 = 3
        return Success()

    def c1s2(self, ctx):
        pass  # pragma: no cover


class DependencyRootMethod(object):
    def c1s1(self, ctx):
        ctx.b1v1 = self.f(ctx.c1v1)
        return Success()

    def c1s2(self, ctx):
        pass  # pragma: no cover
