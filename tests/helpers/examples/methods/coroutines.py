from examples.methods import *  # noqa: F403
from stories import arguments
from stories import Failure
from stories import Next
from stories import Result
from stories import story
from stories import Success

# Mixins.


class MixedCoroutineMethod:
    def one(self, ctx):
        pass  # pragma: no cover

    def two(self, ctx):
        pass  # pragma: no cover

    async def three(self, ctx):
        pass  # pragma: no cover


class MixedFunctionMethod:
    async def one(self, ctx):
        pass  # pragma: no cover

    async def two(self, ctx):
        pass  # pragma: no cover

    def three(self, ctx):
        pass  # pragma: no cover


class NormalMethod:
    async def one(self, ctx):
        return Success()

    async def two(self, ctx):
        return Success()

    async def three(self, ctx):
        return Success()


class FunctionMethod:
    def one(self, ctx):
        pass  # pragma: no cover

    def two(self, ctx):
        pass  # pragma: no cover

    def three(self, ctx):
        pass  # pragma: no cover


# Parent mixins.


class NormalParentMethod:
    async def before(self, ctx):
        return Success()

    async def after(self, ctx):
        return Success()


class FunctionParentMethod:
    def before(self, ctx):
        pass  # pragma: no cover

    def after(self, ctx):
        pass  # pragma: no cover


# Story factories.


def define_coroutine_story():
    class Action:
        @story
        async def do(I):
            pass  # pragma: no cover


# Simple story.


class Simple:
    @story
    @arguments("foo", "bar")
    def x(I):
        I.one
        I.two
        I.three

    async def one(self, ctx):
        return Success()

    async def two(self, ctx):
        if ctx.foo > 1:
            return Failure()

        if ctx.bar < 0:
            return Next()

        if ctx.bar == 10:
            return Next(ctx.bar * 2)

        ctx.baz = 4
        return Success()

    async def three(self, ctx):
        return Result(ctx.bar - ctx.baz)


class Pipe:
    @story
    def x(I):
        I.one
        I.two
        I.three

    @story
    def y(I):
        I.before
        I.x
        I.after

    async def one(self, ctx):
        return Success()

    async def two(self, ctx):
        return Success()

    async def three(self, ctx):
        return Success()

    async def before(self, ctx):
        return Next()

    async def after(self, ctx):
        raise Exception()  # pragma: no cover


class Branch:
    @story
    @arguments("age")
    def show_content(I):
        I.age_lt_18
        I.age_gte_18
        I.load_content

    async def age_lt_18(self, ctx):
        if ctx.age < 18:
            ctx.access_allowed = False
            return Success()
        return Success()

    async def age_gte_18(self, ctx):
        if not hasattr(ctx, "access_allowed") and ctx.age >= 18:
            ctx.access_allowed = True
            return Success()
        return Success()

    async def load_content(self, ctx):
        if ctx.access_allowed:
            return Result("allowed")
        else:
            return Result("denied")


# Dependency injection of the substory.


class SubstoryDI:
    def __init__(self, x):
        self.x = x

    @story
    @arguments("spam")
    def y(I):
        I.start
        I.before
        I.x
        I.after

    async def start(self, ctx):
        ctx.foo = ctx.spam - 1
        return Success()

    async def before(self, ctx):
        ctx.bar = ctx.spam + 1
        return Success()

    async def after(self, ctx):
        return Result(ctx.spam * 2)


# Method tries to return wrong type.


class WrongResult:
    @story
    def x(I):
        I.one

    async def one(self, ctx):
        return 1


# Dependency injection of the implementation methods.


class ImplementationDI:
    def __init__(self, f):
        self.f = f

    @story
    @arguments("foo")
    def x(I):
        I.one

    async def one(self, ctx):
        return Result(self.f(ctx.foo))


# Step error.


class StepError:
    @story
    def x(I):
        I.one

    async def one(self, ctx):
        raise ExpectedException()  # noqa: F405


# Access non-existent context attribute.


class AttributeAccessError:
    @story
    def x(I):
        I.one

    async def one(self, ctx):
        ctx.x
