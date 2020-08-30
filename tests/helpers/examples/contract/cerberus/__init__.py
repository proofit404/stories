from cerberus import Validator

from stories import arguments
from stories import story


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


# Child base classes.


class Child:
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


class ChildWithNull:
    @story
    def x(I):
        I.one


class ChildWithShrink:
    @story
    def x(I):
        I.one

    x.contract(Validator({"baz": {"type": "integer", "coerce": int}}))


class ChildAlias:
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


class ParamChild:
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


class ParamChildWithNull:
    @story
    @arguments("foo", "bar")
    def x(I):
        I.one


class ParamChildWithShrink:
    @story
    @arguments("foo", "bar", "baz")
    def x(I):
        I.one

    x.contract(Validator({"baz": {"type": "integer", "coerce": int}}))


class ParamChildAlias:
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


class NextChildWithSame:
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


class NextParamChildWithString:
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


# Parent base classes.


class Parent:
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


class ParentWithNull:
    @story
    def a(I):
        I.before
        I.x
        I.after


class ParentWithSame:
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


class SequentialParent:
    @story
    def a(I):
        I.before
        I.x
        I.y
        I.after

    a.contract(Validator({}))


class ParamParent:
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


class ParamParentWithNull:
    @story
    @arguments("ham", "eggs")
    def a(I):
        I.before
        I.x
        I.after


class ParamParentWithSame:
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


class ParamParentWithSameWithString:
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


class Root:
    @story
    def i(I):
        I.start
        I.a
        I.finish


Root.i.contract(
    Validator(
        {
            "fizz": {"type": "integer", "coerce": int},
            "buzz": {"type": "integer", "coerce": int},
        }
    )
)


class RootWithSame:
    @story
    def i(I):
        I.start
        I.a
        I.finish


RootWithSame.i.contract(
    Validator(
        {
            "foo": {"type": "integer", "coerce": int},
            "bar": {"type": "list", "schema": {"type": "integer", "coerce": int}},
            "baz": {"type": "integer", "coerce": int},
        }
    )
)


class SequentialRoot:
    @story
    def i(I):
        I.start
        I.a
        I.b
        I.finish


SequentialRoot.i.contract(
    Validator(
        {
            "fizz": {"type": "integer", "coerce": int},
            "buzz": {"type": "integer", "coerce": int},
        }
    )
)


class ParamRoot:
    @story
    @arguments("fizz")
    def i(I):
        I.start
        I.a
        I.finish


ParamRoot.i.contract(
    Validator(
        {
            "fizz": {"type": "integer", "coerce": int},
            "buzz": {"type": "integer", "coerce": int},
        }
    )
)
