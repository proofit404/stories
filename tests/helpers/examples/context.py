from stories import Success, story


# Mixins.


class AssignMethod(object):
    def one(self, ctx):
        ctx.foo = 1


class DeleteMethod(object):
    def one(self, ctx):
        del ctx.foo


# Parent mixins.


class NormalParentMethod(object):
    def before(self, ctx):
        return Success()

    def after(self, ctx):
        return Success()


# Base classes.


class Child(object):
    @story
    def x(I):
        I.one


class Parent(object):
    @story
    def a(I):
        I.before
        I.x
        I.after
