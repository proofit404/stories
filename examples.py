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
    @argument("a")
    @argument("b")
    def x(self):
        self.one()
        self.two()
        self.three()

    def one(self):
        return Success()

    def two(self):
        if self.ctx.a > 1:
            return Failure()

        if self.ctx.b < 0:
            return Skip()

        return Success(c=4)

    def three(self):
        return Result(self.ctx.b - self.ctx.c)


# Substory in the same class.


class SimpleSubstory(Simple):

    @story
    @argument("d")
    def y(self):
        self.before()
        self.x()
        self.after()

    def before(self):
        return Success(a=self.ctx.d - 1, b=self.ctx.d + 1)

    def after(self):
        return Result(self.ctx.d * 2)

    @story
    @argument("a")
    @argument("b")
    def z(self):
        self.first()
        self.x()

    def first(self):
        return Skip()


# Dependency injection of the substory.


class SubstoryDI(object):

    def __init__(self, x):
        self.x = x

    @story
    @argument("d")
    def y(self):
        self.before()
        self.x()
        self.after()

    def before(self):
        return Success(a=self.ctx.d - 1, b=self.ctx.d + 1)

    def after(self):
        return Result(self.ctx.d * 2)


# Method tries to override existed context key.


class ExistedKey(object):

    @story
    @argument("a")
    def x(self):
        self.one()

    def one(self):
        return Success(a=2)


# Method tries to return wrong type.


class WrongResult(object):

    @story
    def x(self):
        self.one()

    def one(self):
        return 1


# Class attribute access.


class AttributeAccess(object):
    clsattr = 1

    @story
    def x(self):
        self.one()

    def one(self):
        return Result(self.clsattr == 1)


# Dependency injection of the implementation methods.


class ImplementationDI(object):

    def __init__(self, f):
        self.f = f

    @story
    @argument("a")
    def x(self):
        self.one()

    def one(self):
        return Result(self.f(self.ctx.a))


# Context representation.


class SimpleCtxRepr(object):

    @story
    @argument("a")
    def x(self):
        self.one()
        self.two()
        self.three()
        self.four()

    def one(self):
        return Success(b=1)

    def two(self):
        return Success(c=2)

    def three(self):
        return Success(d=3)

    def four(self):
        return Result(repr(self.ctx))


class SimpleSubstoryCtxRepr(SimpleCtxRepr):

    @story
    @argument("e")
    def y(self):
        self.before()
        self.x()

    def before(self):
        return Success(a=0)


class SubstoryDICtxRepr(object):

    def __init__(self, x):
        self.x = x

    @story
    @argument("e")
    def y(self):
        self.before()
        self.x()

    def before(self):
        return Success(a=0)
