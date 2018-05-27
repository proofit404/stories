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

    def one(self):
        return Success()

    def two(self):
        if self.ctx.foo > 1:
            return Failure()

        if self.ctx.bar < 0:
            return Skip()

        return Success(baz=4)

    def three(self):
        return Result(self.ctx.bar - self.ctx.baz)


# Substory in the same class.


class SimpleSubstory(Simple):

    @story
    @argument("spam")
    def y(self):
        self.before()
        self.x()
        self.after()

    def before(self):
        return Success(foo=self.ctx.spam - 1, bar=self.ctx.spam + 1)

    def after(self):
        return Result(self.ctx.spam * 2)

    @story
    @argument("foo")
    @argument("bar")
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
    @argument("spam")
    def y(self):
        self.before()
        self.x()
        self.after()

    def before(self):
        return Success(foo=self.ctx.spam - 1, bar=self.ctx.spam + 1)

    def after(self):
        return Result(self.ctx.spam * 2)


# Method tries to override existed context key.


class ExistedKey(object):

    @story
    @argument("foo")
    def x(self):
        self.one()

    def one(self):
        return Success(foo=2)


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
    @argument("foo")
    def x(self):
        self.one()

    def one(self):
        return Result(self.f(self.ctx.foo))


# Context representation.


class SimpleCtxRepr(object):

    @story
    @argument("aaaa")
    def x(self):
        self.one()
        self.two()
        self.three()
        self.four()

    def one(self):
        return Success(bbb=1)

    def two(self):
        return Success(c=2)

    def three(self):
        return Success(dd=3)

    def four(self):
        return Result(repr(self.ctx))


class SimpleSubstoryCtxRepr(SimpleCtxRepr):

    @story
    @argument("e")
    def y(self):
        self.before()
        self.x()

    def before(self):
        return Success(aaaa=0)


class SubstoryDICtxRepr(object):

    def __init__(self, x):
        self.x = x

    @story
    @argument("e")
    def y(self):
        self.before()
        self.x()

    def before(self):
        return Success(aaaa=0)
