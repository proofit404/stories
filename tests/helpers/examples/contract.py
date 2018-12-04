from stories import Success, argument, story


# Method tries to override existed context key.


class ExistedKey(object):
    @story
    @argument("foo")
    @argument("bar")
    def x(I):
        I.one

    def one(self, ctx):
        return Success(foo=2, bar=1)
