from cerberus import Validator

from stories import Success, arguments, story
from stories.shortcuts import contract_in


# Mixins.


class NormalMethod(object):
    def one(self, ctx):
        return Success()


class StringMethod(object):
    def one(self, ctx):
        return Success(foo="1", bar=["2"])


class WrongMethod(object):
    def one(self, ctx):
        return Success(foo="<boom>", bar=["<boom>"])


class UnknownMethod(object):
    def one(self, ctx):
        return Success(spam="0", quiz="1")


class ExceptionMethod(object):
    def one(self, ctx):
        raise Exception


# Parent mixins.


class NormalParentMethod(object):
    def before(self, ctx):
        return Success()

    def after(self, ctx):
        return Success()


class StringParentMethod(object):
    def before(self, ctx):
        return Success(foo="1", bar=["2"])

    def after(self, ctx):
        return Success()


class ExceptionParentMethod(object):
    def before(self, ctx):
        raise Exception

    def after(self, ctx):
        return Success()


# Root mixins.


class NormalRootMethod(object):
    def start(self, ctx):
        return Success()

    def finish(self, ctx):
        return Success()


class StringRootMethod(object):
    def start(self, ctx):
        return Success(foo="1", bar=["2"])

    def finish(self, ctx):
        return Success()


class ExceptionRootMethod(object):
    def start(self, ctx):
        raise Exception

    def finish(self, ctx):
        return Success()


# Base classes.


class Child(object):
    @story
    def x(I):
        I.one

    x.contract(
        Validator(
            {
                "foo": {"type": "integer", "coerce": int},
                "bar": {"type": "list", "schema": {"type": "integer", "coerce": int}},
                "baz": {"type": "integer", "coerce": int},
            }
        )
    )


class ChildWithNull(object):
    @story
    def x(I):
        I.one


class ChildReuse(object):
    @story
    def x(I):
        I.one


class ParamChild(object):
    @story
    @arguments("foo", "bar")
    def x(I):
        I.one

    x.contract(
        Validator(
            {
                "foo": {"type": "integer", "coerce": int},
                "bar": {"type": "list", "schema": {"type": "integer", "coerce": int}},
                "baz": {"type": "integer", "coerce": int},
            }
        )
    )


class NextChildWithSame(object):
    @story
    def y(I):
        I.one

    y.contract(
        Validator(
            {
                "foo": {"type": "integer", "coerce": int},
                "bar": {"type": "list", "schema": {"type": "integer", "coerce": int}},
                "baz": {"type": "integer", "coerce": int},
            }
        )
    )


class NextParamChildWithString(object):
    @story
    @arguments("foo", "bar")
    def y(I):
        I.one

    y.contract(
        Validator(
            {
                "foo": {"type": "string"},
                "bar": {"type": "list", "schema": {"type": "string"}},
            }
        )
    )


class ParamChildWithNull(object):
    @story
    @arguments("foo", "bar")
    def x(I):
        I.one


class ParamChildWithShrink(object):
    @story
    @arguments("foo", "bar", "baz")
    def x(I):
        I.one

    x.contract(Validator({"baz": {"type": "integer", "coerce": int}}))


# Parent base classes.


class Parent(object):
    @story
    def a(I):
        I.before
        I.x
        I.after


Parent.a.contract(
    Validator(
        {
            "ham": {"type": "integer", "coerce": int},
            "eggs": {"type": "integer", "coerce": int},
            "beans": {"type": "integer", "coerce": int},
        }
    )
)


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


ParentWithSame.a.contract(
    Validator(
        {
            "foo": {"type": "integer", "coerce": int},
            "bar": {"type": "list", "schema": {"type": "integer", "coerce": int}},
            "baz": {"type": "integer", "coerce": int},
        }
    )
)


class ParentReuse(object):
    @story
    def a(I):
        I.before
        I.x
        I.after


ChildReuse.x.contract(
    ParentReuse.a.contract(
        Validator(
            {
                "foo": {"type": "integer", "coerce": int},
                "bar": {"type": "list", "schema": {"type": "integer", "coerce": int}},
                "baz": {"type": "integer", "coerce": int},
            }
        )
    )
)


class SequentialParent(object):
    @story
    def a(I):
        I.before
        I.x
        I.y
        I.after

    a.contract(Validator({}))


class ParamParent(object):
    @story
    @arguments("ham", "eggs")
    def a(I):
        I.before
        I.x
        I.after


ParamParent.a.contract(
    Validator(
        {
            "ham": {"type": "integer", "coerce": int},
            "eggs": {"type": "integer", "coerce": int},
            "beans": {"type": "integer", "coerce": int},
        }
    )
)


class ParamParentWithNull(object):
    @story
    @arguments("ham", "eggs")
    def a(I):
        I.before
        I.x
        I.after


class ParamParentWithSameWithString(object):
    @story
    @arguments("foo", "bar")
    def a(I):
        I.before
        I.x
        I.after


ParamParentWithSameWithString.a.contract(
    Validator(
        {
            "foo": {"type": "string"},
            "bar": {"type": "list", "schema": {"type": "string"}},
        }
    )
)


# Root base classes.


class Root(object):
    @story
    def i(I):
        I.start
        I.a
        I.finish


contract_in(
    Root,
    Validator(
        {
            "fizz": {"type": "integer", "coerce": int},
            "buzz": {"type": "integer", "coerce": int},
        }
    ),
)


class RootWithSame(object):
    @story
    def i(I):
        I.start
        I.a
        I.finish


contract_in(
    RootWithSame,
    Validator(
        {
            "foo": {"type": "integer", "coerce": int},
            "bar": {"type": "list", "schema": {"type": "integer", "coerce": int}},
            "baz": {"type": "integer", "coerce": int},
        }
    ),
)


class ParamRoot(object):
    @story
    @arguments("fizz")
    def i(I):
        I.start
        I.a
        I.finish


contract_in(
    ParamRoot,
    Validator(
        {
            "fizz": {"type": "integer", "coerce": int},
            "buzz": {"type": "integer", "coerce": int},
        }
    ),
)
