from cerberus import Validator

from stories import Success, arguments, story


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

    contract = x.contract(
        Validator(
            {
                "foo": {"type": "integer", "coerce": int},
                "bar": {"type": "integer", "coerce": int},
                "baz": {"type": "integer", "coerce": int},
            }
        )
    )


class ChildWithNull(object):
    @story
    def x(I):
        I.one


class ParamChild(object):
    @story
    @arguments("foo", "bar")
    def x(I):
        I.one

    contract = x.contract(
        Validator(
            {
                "foo": {"type": "integer", "coerce": int},
                "bar": {"type": "integer", "coerce": int},
                "baz": {"type": "integer", "coerce": int},
            }
        )
    )


class ParamChildWithNull(object):
    @story
    @arguments("foo", "bar")
    def x(I):
        I.one


class ParentWithNull(object):
    @story
    def a(I):
        I.before
        I.x
        I.after


class ParamParent(object):
    @story
    @arguments("foo", "bar")
    def a(I):
        I.before
        I.x
        I.after

    contract = a.contract(
        Validator(
            {
                "foo": {"type": "integer", "coerce": int},
                "bar": {"type": "integer", "coerce": int},
                "baz": {"type": "integer", "coerce": int},
            }
        )
    )


class ParamParentWithNull(object):
    @story
    @arguments("foo", "bar")
    def a(I):
        I.before
        I.x
        I.after
