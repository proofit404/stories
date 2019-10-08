from cerberus import Validator

from stories import arguments
from stories import story
from stories import Success
from stories.shortcuts import contract_in


# Constants.


representations = {
    "int_error": """
  field '{}' cannot be coerced: invalid literal for int() with base 10: '<boom>'
  must be of integer type
    """.strip(),
    "list_of_int_error": """  0:
      must be of integer type
      field '0' cannot be coerced: invalid literal for int() with base 10: '<boom>'
    """.rstrip(),
    "int_field_repr": "integer",
    "str_field_repr": "string",
    "list_of_int_field_repr": "list[integer]",
    "list_of_str_field_repr": "list[string]",
    "contract_class_repr": "<class 'cerberus.validator.Validator'>",
}


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


class AliasMethod(object):
    def one(self, ctx):
        value = {"key": "1"}
        return Success(foo=value, bar=value, baz=value)


# Next child mixins.


class NormalNextMethod(object):
    def two(self, ctx):
        return Success()


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


class StringWideRootMethod(object):
    def start(self, ctx):
        return Success(foo="1", bar=["2"], baz="1")

    def finish(self, ctx):
        return Success()


class ExceptionRootMethod(object):
    def start(self, ctx):
        raise Exception

    def finish(self, ctx):
        return Success()


# Child base classes.


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


class ChildWithShrink(object):
    @story
    def x(I):
        I.one

    x.contract(Validator({"baz": {"type": "integer", "coerce": int}}))


class ChildReuse(object):
    @story
    def x(I):
        I.one


class ChildAlias(object):
    @story
    def x(I):
        I.one

    x.contract(
        Validator(
            {
                "foo": {"type": "dict", "schema": {"key": {"type": "string"}}},
                "bar": {"type": "dict", "schema": {"key": {"type": "string"}}},
                "baz": {
                    "type": "dict",
                    "schema": {"key": {"type": "integer", "coerce": int}},
                },
            }
        )
    )


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


class ParamChildAlias(object):
    @story
    @arguments("foo", "bar", "baz")
    def x(I):
        I.one

    x.contract(
        Validator(
            {
                "foo": {"type": "dict", "schema": {"key": {"type": "string"}}},
                "bar": {"type": "dict", "schema": {"key": {"type": "string"}}},
                "baz": {
                    "type": "dict",
                    "schema": {"key": {"type": "integer", "coerce": int}},
                },
            }
        )
    )


# Next child base classes.


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
        I.two

    y.contract(
        Validator(
            {
                "foo": {"type": "string"},
                "bar": {"type": "list", "schema": {"type": "string"}},
            }
        )
    )


class NextParamChildReuse(object):
    @story
    @arguments("foo", "bar", "baz")
    def y(I):
        I.one


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


class ParamParentWithSame(object):
    @story
    @arguments("foo", "bar", "baz")
    def a(I):
        I.before
        I.after


ParamParentWithSame.a.contract(
    Validator(
        {
            "foo": {"type": "integer", "coerce": int},
            "bar": {"type": "list", "schema": {"type": "integer", "coerce": int}},
            "baz": {"type": "integer", "coerce": int},
        }
    )
)


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


# Next parent base classes.


class NextParamParentReuse(object):
    @story
    @arguments("foo", "bar")
    def b(I):
        I.before
        I.y
        I.after


NextParamChildReuse.y.contract(
    NextParamParentReuse.b.contract(
        Validator(
            {
                "foo": {"type": "integer", "coerce": int},
                "bar": {"type": "list", "schema": {"type": "integer", "coerce": int}},
                "baz": {"type": "integer", "coerce": int},
            }
        )
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


class SequentialRoot(object):
    @story
    def i(I):
        I.start
        I.a
        I.b
        I.finish


contract_in(
    SequentialRoot,
    Validator(
        {
            "fizz": {"type": "integer", "coerce": int},
            "buzz": {"type": "integer", "coerce": int},
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
