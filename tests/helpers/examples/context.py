from stories import arguments
from stories import Result
from stories import story
from stories import Success


# Mixins.


class NormalMethod(object):
    def one(self, ctx):
        return Success(foo=self.foo)


class AssignMethod(object):
    def one(self, ctx):
        ctx.foo = 1


class DeleteMethod(object):
    def one(self, ctx):
        del ctx.foo


class CompareMethod(object):
    def one(self, ctx):
        if ctx:
            pass


class DirMethod(object):
    def one(self, ctx):
        return Result(dir(ctx))


# Parent mixins.


class NormalParentMethod(object):
    def before(self, ctx):
        return Success()

    def after(self, ctx):
        return Success()


class DirParentMethod(object):
    def before(self, ctx):
        return Success()

    def after(self, ctx):
        return Result(dir(ctx))


# Base classes.


class Child(object):
    @story
    def x(I):
        I.one


class ParamChild(object):
    @story
    @arguments("bar")
    def x(I):
        I.one


class Parent(object):
    @story
    def a(I):
        I.before
        I.x
        I.after


class ParamParent(object):
    @story
    @arguments("bar")
    def a(I):
        I.before
        I.x
        I.after
