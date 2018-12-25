from stories import Success, arguments, story


# Method tries to override existed context key.


class ExistedKey(object):
    @story
    @arguments("foo", "bar")
    def x(I):
        I.one

    def one(self, ctx):
        return Success(foo=2, bar=1)


class SubstoryExistedKey(ExistedKey):
    @story
    @arguments("foo", "bar")
    def a(I):
        I.x


class ExistedKeyDI(object):
    def __init__(self):
        self.x = ExistedKey().x

    @story
    @arguments("foo", "bar")
    def a(I):
        I.x


# Method tries to assign attribute to the context object.


class AssignAttribute(object):
    @story
    def x(I):
        I.one

    def one(self, ctx):
        ctx.foo = 1


class DeleteAttribute(object):
    @story
    @arguments("foo")
    def x(I):
        I.one

    def one(self, ctx):
        del ctx.foo
