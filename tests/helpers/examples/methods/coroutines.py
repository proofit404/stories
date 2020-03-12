# -*- coding: utf-8 -*-
from examples.methods import *  # noqa: F403
from stories import arguments
from stories import Failure
from stories import Result
from stories import Skip
from stories import story
from stories import Success


# Mixins.


class MixedCoroutineMethod(object):
    def one(self, ctx):
        pass  # pragma: no cover

    def two(self, ctx):
        pass  # pragma: no cover

    async def three(self, ctx):
        pass  # pragma: no cover


class MixedFunctionMethod(object):
    async def one(self, ctx):
        pass  # pragma: no cover

    async def two(self, ctx):
        pass  # pragma: no cover

    def three(self, ctx):
        pass  # pragma: no cover


class NormalMethod(object):
    async def one(self, ctx):
        return Success()

    async def two(self, ctx):
        return Success()

    async def three(self, ctx):
        return Success()


class FunctionMethod(object):
    def one(self, ctx):
        pass  # pragma: no cover

    def two(self, ctx):
        pass  # pragma: no cover

    def three(self, ctx):
        pass  # pragma: no cover


# Parent mixins.


class NormalParentMethod(object):
    async def before(self, ctx):
        return Success()

    async def after(self, ctx):
        return Success()


class FunctionParentMethod(object):
    def before(self, ctx):
        pass  # pragma: no cover

    def after(self, ctx):
        pass  # pragma: no cover


# Story factories.


def define_coroutine_story():
    class Action(object):
        @story
        async def do(I):
            pass


# Simple story.


class Simple(object):
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
            return Skip()

        return Success(baz=4)

    async def three(self, ctx):
        return Result(ctx.bar - ctx.baz)


class Pipe(object):
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
        return Skip()

    async def after(self, ctx):
        raise Exception()  # pragma: no cover


class Branch(object):
    @story
    @arguments("age")
    def show_content(I):
        I.age_lt_18
        I.age_gte_18
        I.load_content

    async def age_lt_18(self, ctx):
        if ctx.age < 18:
            return Success(access_allowed=False)
        return Success()

    async def age_gte_18(self, ctx):
        if not hasattr(ctx, "access_allowed") and ctx.age >= 18:
            return Success(access_allowed=True)
        return Success()

    async def load_content(self, ctx):
        if ctx.access_allowed:
            return Result("allowed")
        else:
            return Result("denied")


# Substory in the same class.


class SimpleSubstory(Simple):
    @story
    @arguments("spam")
    def y(I):
        I.start
        I.before
        I.x
        I.after

    async def start(self, ctx):
        return Success(foo=ctx.spam - 1)

    async def before(self, ctx):
        return Success(bar=ctx.spam + 1)

    async def after(self, ctx):
        return Result(ctx.spam * 2)

    @story
    @arguments("foo", "bar")
    def z(I):
        I.first
        I.x

    async def first(self, ctx):
        return Skip()


# Dependency injection of the substory.


class SubstoryDI(object):
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
        return Success(foo=ctx.spam - 1)

    async def before(self, ctx):
        return Success(bar=ctx.spam + 1)

    async def after(self, ctx):
        return Result(ctx.spam * 2)


# Method tries to return wrong type.


class WrongResult(object):
    @story
    def x(I):
        I.one

    async def one(self, ctx):
        return 1


# Dependency injection of the implementation methods.


class ImplementationDI(object):
    def __init__(self, f):
        self.f = f

    @story
    @arguments("foo")
    def x(I):
        I.one

    async def one(self, ctx):
        return Result(self.f(ctx.foo))


# Step error.


class StepError(object):
    @story
    def x(I):
        I.one

    async def one(self, ctx):
        raise ExpectedException()  # noqa: F405


# Access non-existent context attribute.


class AttributeAccessError(object):
    @story
    def x(I):
        I.one

    async def one(self, ctx):
        ctx.x


class ParallelStory(object):
    @story
    def x(I):
        with I.parallel as p:
            p.one
            p.two

    async def one(self, ctx):
        return Success()

    async def two(self, ctx):
        return Success()


class ParallelStoryWithNestedStory(object):
    @story
    def x(I):
        with I.parallel as p:
            p.one
            p.two
            p.y

    async def one(self, ctx):
        return Success()

    async def two(self, ctx):
        return Success()

    @story
    def y(I):
        I.one
        I.two


class ParallelStoryWithNestedParallelStory(object):
    @story
    def y(I):
        I.one
        with I.parallel as p:
            p.one
            p.two

    @story
    def x(I):
        with I.parallel as p:
            p.one
            p.two
            p.y

    async def one(self, ctx):
        return Success()

    async def two(self, ctx):
        return Success()
