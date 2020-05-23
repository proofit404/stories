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
    def a1(I):
        I.a1s1

    a1.contract(
        Validator(
            {
                "a1v1": {"type": "integer", "coerce": int},
                "a1v2": {"type": "list", "schema": {"type": "integer", "coerce": int}},
                "a1v3": {"type": "integer", "coerce": int},
            }
        )
    )


class ChildWithNull:
    @story
    def a1(I):
        I.a1s1


class ChildWithShrink:
    @story
    def a1(I):
        I.a1s1

    a1.contract(Validator({"a1v3": {"type": "integer", "coerce": int}}))


class ChildAlias:
    @story
    def a1(I):
        I.a1s1

    a1.contract(
        Validator(
            {
                "a1v1": {"type": "dict", "schema": {"key": {"type": "string"}}},
                "a1v2": {"type": "dict", "schema": {"key": {"type": "string"}}},
                "a1v3": {
                    "type": "dict",
                    "schema": {"key": {"type": "integer", "coerce": int}},
                },
            }
        )
    )


class ParamChild:
    @story
    @arguments("a1v1", "a1v2")
    def a1(I):
        I.a1s1

    a1.contract(
        Validator(
            {
                "a1v1": {"type": "integer", "coerce": int},
                "a1v2": {"type": "list", "schema": {"type": "integer", "coerce": int}},
                "a1v3": {"type": "integer", "coerce": int},
            }
        )
    )


class ParamChildWithNull:
    @story
    @arguments("a1v1", "a1v2")
    def a1(I):
        I.a1s1


class ParamChildWithShrink:
    @story
    @arguments("a1v1", "a1v2", "a1v3")
    def a1(I):
        I.a1s1

    a1.contract(Validator({"a1v3": {"type": "integer", "coerce": int}}))


class ParamChildAlias:
    @story
    @arguments("a1v1", "a1v2", "a1v3")
    def a1(I):
        I.a1s1

    a1.contract(
        Validator(
            {
                "a1v1": {"type": "dict", "schema": {"key": {"type": "string"}}},
                "a1v2": {"type": "dict", "schema": {"key": {"type": "string"}}},
                "a1v3": {
                    "type": "dict",
                    "schema": {"key": {"type": "integer", "coerce": int}},
                },
            }
        )
    )


# Next child base classes.


class NextChildWithSame:
    @story
    def a2(I):
        I.a1s1

    a2.contract(
        Validator(
            {
                "a1v1": {"type": "integer", "coerce": int},
                "a1v2": {"type": "list", "schema": {"type": "integer", "coerce": int}},
                "a1v3": {"type": "integer", "coerce": int},
            }
        )
    )


class NextParamChildWithString:
    @story
    @arguments("a1v1", "a1v2")
    def a2(I):
        I.a2s1

    a2.contract(
        Validator(
            {
                "a1v1": {"type": "string"},
                "a1v2": {"type": "list", "schema": {"type": "string"}},
            }
        )
    )


# Parent base classes.


class Parent:
    @story
    def b1(I):
        I.b1s1
        I.a1
        I.b1s2


Parent.b1.contract(
    Validator(
        {
            "b1v1": {"type": "integer", "coerce": int},
            "b1v2": {"type": "integer", "coerce": int},
            "b1v3": {"type": "integer", "coerce": int},
        }
    )
)


class ParentWithNull:
    @story
    def b1(I):
        I.b1s1
        I.a1
        I.b1s2


class ParentWithSame:
    @story
    def b1(I):
        I.b1s1
        I.a1
        I.b1s2


ParentWithSame.b1.contract(
    Validator(
        {
            "a1v1": {"type": "integer", "coerce": int},
            "a1v2": {"type": "list", "schema": {"type": "integer", "coerce": int}},
            "a1v3": {"type": "integer", "coerce": int},
        }
    )
)


class SequentialParent:
    @story
    def b1(I):
        I.b1s1
        I.a1
        I.a2
        I.b1s2

    b1.contract(Validator({}))


class ParamParent:
    @story
    @arguments("b1v1", "b1v2")
    def b1(I):
        I.b1s1
        I.a1
        I.b1s2


ParamParent.b1.contract(
    Validator(
        {
            "b1v1": {"type": "integer", "coerce": int},
            "b1v2": {"type": "integer", "coerce": int},
            "b1v3": {"type": "integer", "coerce": int},
        }
    )
)


class ParamParentWithNull:
    @story
    @arguments("b1v1", "b1v2")
    def b1(I):
        I.b1s1
        I.a1
        I.b1s2


class ParamParentWithSame:
    @story
    @arguments("a1v1", "a1v2", "a1v3")
    def b1(I):
        I.b1s1
        I.b1s2


ParamParentWithSame.b1.contract(
    Validator(
        {
            "a1v1": {"type": "integer", "coerce": int},
            "a1v2": {"type": "list", "schema": {"type": "integer", "coerce": int}},
            "a1v3": {"type": "integer", "coerce": int},
        }
    )
)


class ParamParentWithSameWithString:
    @story
    @arguments("a1v1", "a1v2")
    def b1(I):
        I.b1s1
        I.a1
        I.b1s2


ParamParentWithSameWithString.b1.contract(
    Validator(
        {
            "a1v1": {"type": "string"},
            "a1v2": {"type": "list", "schema": {"type": "string"}},
        }
    )
)


# Root base classes.


class Root:
    @story
    def c1(I):
        I.c1s1
        I.b1
        I.c1s2


Root.c1.contract(
    Validator(
        {
            "c1v1": {"type": "integer", "coerce": int},
            "c1v2": {"type": "integer", "coerce": int},
        }
    )
)


class RootWithSame:
    @story
    def c1(I):
        I.c1s1
        I.b1
        I.c1s2


RootWithSame.c1.contract(
    Validator(
        {
            "a1v1": {"type": "integer", "coerce": int},
            "a1v2": {"type": "list", "schema": {"type": "integer", "coerce": int}},
            "a1v3": {"type": "integer", "coerce": int},
        }
    )
)


class SequentialRoot:
    @story
    def c1(I):
        I.c1s1
        I.b1
        I.b2
        I.c1s2


SequentialRoot.c1.contract(
    Validator(
        {
            "c1v1": {"type": "integer", "coerce": int},
            "c1v2": {"type": "integer", "coerce": int},
        }
    )
)


class ParamRoot:
    @story
    @arguments("c1v1")
    def c1(I):
        I.c1s1
        I.b1
        I.c1s2


ParamRoot.c1.contract(
    Validator(
        {
            "c1v1": {"type": "integer", "coerce": int},
            "c1v2": {"type": "integer", "coerce": int},
        }
    )
)
