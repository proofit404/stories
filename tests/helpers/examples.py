from stories import Failure, Result, Skip, Success, argument, story


# Empty story.


class Empty(object):
    @story
    def x(self):
        pass


# Empty substory.


class EmptySubstory(Empty):
    @story
    def y(self):
        self.x()


# Simple story.


class Simple(object):
    @story
    @argument("foo")
    @argument("bar")
    def x(self):
        self.one()
        self.two()
        self.three()

    def one(self, ctx):
        return Success()

    def two(self, ctx):
        if ctx.foo > 2:
            return Failure("'foo' is too big")

        if ctx.foo > 1:
            return Failure()

        if ctx.bar < 0:
            return Skip()

        return Success(baz=4)

    def three(self, ctx):
        return Result(ctx.bar - ctx.baz)


# Substory in the same class.


class SimpleSubstory(Simple):
    @story
    @argument("spam")
    def y(self):
        self.start()
        self.before()
        self.x()
        self.after()

    def start(self, ctx):
        return Success(foo=ctx.spam - 1)

    def before(self, ctx):
        return Success(bar=ctx.spam + 1)

    def after(self, ctx):
        return Result(ctx.spam * 2)

    @story
    @argument("foo")
    @argument("bar")
    def z(self):
        self.first()
        self.x()

    def first(self, ctx):
        return Skip()


# Dependency injection of the substory.


class SubstoryDI(object):
    def __init__(self, x):
        self.x = x

    @story
    @argument("spam")
    def y(self):
        self.start()
        self.before()
        self.x()
        self.after()

    def start(self, ctx):
        return Success(foo=ctx.spam - 1)

    def before(self, ctx):
        return Success(bar=ctx.spam + 1)

    def after(self, ctx):
        return Result(ctx.spam * 2)


# Method tries to override existed context key.


class ExistedKey(object):
    @story
    @argument("foo")
    def x(self):
        self.one()

    def one(self, ctx):
        return Success(foo=2)


# Method tries to return wrong type.


class WrongResult(object):
    @story
    def x(self):
        self.one()

    def one(self, ctx):
        return 1


# Class attribute access.


class AttributeAccess(object):
    clsattr = 1

    @story
    def x(self):
        self.one()

    def one(self, ctx):
        self.clsattr


# Dependency injection of the implementation methods.


class ImplementationDI(object):
    def __init__(self, f):
        self.f = f

    @story
    @argument("foo")
    def x(self):
        self.one()

    def one(self, ctx):
        return Result(self.f(ctx.foo))


# Step error.


class StepError(object):
    @story
    def x(self):
        self.one()

    def one(self, ctx):
        raise Exception()
