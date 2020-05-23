from operator import itemgetter

from stories import arguments
from stories import story


# Constants.


representations = {
    "int_error": "Invalid value",
    "list_of_int_error": "Invalid value",
    "int_field_repr": "integer",
    "str_field_repr": "string",
    "list_of_int_field_repr": "list_of(integer)",
    "list_of_str_field_repr": "list_of(string)",
    "contract_class_repr": repr(dict),
}


# Helper functions.


def integer(value):
    if isinstance(value, int):
        return value, None
    elif isinstance(value, str) and value.isdigit():
        return int(value), None
    else:
        return None, "Invalid value"


def string(value):
    if isinstance(value, str):
        return value, None
    else:
        return None, "Invalid value"


def list_of(f):
    def validator(value):
        if isinstance(value, list):
            new = list(map(f, value))
            if any(map(itemgetter(1), new)):
                return None, "Invalid value"
            else:
                return list(map(itemgetter(0), new)), None
        else:
            return None, "Invalid value"

    validator.__name__ = "list_of(" + f.__name__ + ")"
    return validator


def dict_of(k, v):
    def validator(value):
        if isinstance(value, dict):
            new_key = list(map(k, value.keys()))
            new_value = list(map(v, value.values()))
            if any(map(itemgetter(1), new_key)) or any(map(itemgetter(1), new_value)):
                return None, "Invalid value"
            else:
                return {k(a1)[0]: v(a2)[0] for a1, a2 in value.items()}, None
        else:
            return None, "Invalid value"

    validator.__name__ = "dict_of(" + k.__name__ + ", " + v.__name__ + ")"
    return validator


# Child base classes.


class Child:
    @story
    def a1(I):
        I.a1s1

    a1.contract({"a1v1": integer, "a1v2": list_of(integer), "a1v3": integer})


class ChildWithNull:
    @story
    def a1(I):
        I.a1s1


class ChildWithShrink:
    @story
    def a1(I):
        I.a1s1

    a1.contract({"a1v3": integer})


class ChildAlias:
    @story
    def a1(I):
        I.a1s1

    a1.contract(
        {
            "a1v1": dict_of(string, string),
            "a1v2": dict_of(string, string),
            "a1v3": dict_of(string, integer),
        }
    )


class ParamChild:
    @story
    @arguments("a1v1", "a1v2")
    def a1(I):
        I.a1s1

    a1.contract({"a1v1": integer, "a1v2": list_of(integer), "a1v3": integer})


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

    a1.contract({"a1v3": integer})


class ParamChildAlias:
    @story
    @arguments("a1v1", "a1v2", "a1v3")
    def a1(I):
        I.a1s1

    a1.contract(
        {
            "a1v1": dict_of(string, string),
            "a1v2": dict_of(string, string),
            "a1v3": dict_of(string, integer),
        }
    )


# Next child base classes.


class NextChildWithSame:
    @story
    def a2(I):
        I.a1s1

    a2.contract({"a1v1": integer, "a1v2": list_of(integer), "a1v3": integer})


class NextParamChildWithString:
    @story
    @arguments("a1v1", "a1v2")
    def a2(I):
        I.a2s1

    a2.contract({"a1v1": string, "a1v2": list_of(string)})


# Parent base classes.


class Parent:
    @story
    def b1(I):
        I.b1s1
        I.a1
        I.b1s2


Parent.b1.contract({"b1v1": integer, "b1v2": integer, "b1v3": integer})


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


ParentWithSame.b1.contract({"a1v1": integer, "a1v2": list_of(integer), "a1v3": integer})


class SequentialParent:
    @story
    def b1(I):
        I.b1s1
        I.a1
        I.a2
        I.b1s2

    b1.contract({})


class ParamParent:
    @story
    @arguments("b1v1", "b1v2")
    def b1(I):
        I.b1s1
        I.a1
        I.b1s2


ParamParent.b1.contract({"b1v1": integer, "b1v2": integer, "b1v3": integer})


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
    {"a1v1": integer, "a1v2": list_of(integer), "a1v3": integer}
)


class ParamParentWithSameWithString:
    @story
    @arguments("a1v1", "a1v2")
    def b1(I):
        I.b1s1
        I.a1
        I.b1s2


ParamParentWithSameWithString.b1.contract({"a1v1": string, "a1v2": list_of(string)})


# Root base classes.


class Root:
    @story
    def c1(I):
        I.c1s1
        I.b1
        I.c1s2


Root.c1.contract({"c1v1": integer, "c1v2": integer})


class RootWithSame:
    @story
    def c1(I):
        I.c1s1
        I.b1
        I.c1s2


RootWithSame.c1.contract({"a1v1": integer, "a1v2": list_of(integer), "a1v3": integer})


class SequentialRoot:
    @story
    def c1(I):
        I.c1s1
        I.b1
        I.b2
        I.c1s2


SequentialRoot.c1.contract({"c1v1": integer, "c1v2": integer})


class ParamRoot:
    @story
    @arguments("c1v1")
    def c1(I):
        I.c1s1
        I.b1
        I.c1s2


ParamRoot.c1.contract({"c1v1": integer, "c1v2": integer})
