from stories import Success, arguments, story


# Helper functions.


def integer(value):
    if isinstance(value, int):
        return value, None
    elif isinstance(value, str) and value.isdigit():
        return int(value), None
    else:
        return None, "Invalid value"


# Mixins.


class NormalMethod(object):
    def one(self, ctx):
        return Success()


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

    contract = x.contract({"foo": integer, "bar": integer, "baz": integer})


class ChildWithNull(object):
    @story
    def x(I):
        I.one


class ParamChild(object):
    @story
    @arguments("foo", "bar")
    def x(I):
        I.one

    contract = x.contract({"foo": integer, "bar": integer, "baz": integer})


class ParamChildWithNull(object):
    @story
    @arguments("foo", "bar")
    def x(I):
        I.one


# Parent base classes.


class ParentWithNull(object):
    @story
    def a(I):
        I.before
        I.x
        I.after


class ParentWithSame(object):
    @story
    def a(I):
        I.before
        I.x
        I.after


ParentWithSame.a.contract({"foo": integer, "bar": integer, "baz": integer})


class ParamParent(object):
    @story
    @arguments("foo", "bar")
    def a(I):
        I.before
        I.x
        I.after


ParamParent.a.contract({"foo": integer, "bar": integer, "baz": integer})


class ParamParentWithNull(object):
    @story
    @arguments("foo", "bar")
    def a(I):
        I.before
        I.x
        I.after
