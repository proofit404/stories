from stories import Success, story


# Mixins.


class StringMethod(object):
    def one(self, ctx):
        return Success(foo="1", bar="2")


class WrongMethod(object):
    def one(self, ctx):
        return Success(foo="<boom>", bar="<boom>")


class UnknownMethod(object):
    def one(self, ctx):
        return Success(spam="0", quiz="1")


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

    contract = x.contract(
        {
            "foo": lambda value: isinstance(value, int),
            "bar": lambda value: isinstance(value, int),
            "baz": lambda value: isinstance(value, int),
        }
    )


class ParentWithNull(object):
    @story
    def a(I):
        I.before
        I.x
        I.after
