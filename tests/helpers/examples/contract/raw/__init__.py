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
                return {k(x)[0]: v(y)[0] for x, y in value.items()}, None
        else:
            return None, "Invalid value"

    validator.__name__ = "dict_of(" + k.__name__ + ", " + v.__name__ + ")"
    return validator


# Child base classes.


class Child:
    @story
    def x(I):
        I.one

    x.contract({"foo": integer, "bar": list_of(integer), "baz": integer})


class ChildWithNull:
    @story
    def x(I):
        I.one


class ChildWithShrink:
    @story
    def x(I):
        I.one

    x.contract({"baz": integer})


class ChildAlias:
    @story
    def x(I):
        I.one

    x.contract(
        {
            "foo": dict_of(string, string),
            "bar": dict_of(string, string),
            "baz": dict_of(string, integer),
        }
    )


class ParamChild:
    @story
    @arguments("foo", "bar")
    def x(I):
        I.one

    x.contract({"foo": integer, "bar": list_of(integer), "baz": integer})


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

    x.contract({"baz": integer})


class ParamChildAlias:
    @story
    @arguments("foo", "bar", "baz")
    def x(I):
        I.one

    x.contract(
        {
            "foo": dict_of(string, string),
            "bar": dict_of(string, string),
            "baz": dict_of(string, integer),
        }
    )


# Next child base classes.


class NextChildWithSame:
    @story
    def y(I):
        I.one

    y.contract({"foo": integer, "bar": list_of(integer), "baz": integer})


class NextParamChildWithString:
    @story
    @arguments("foo", "bar")
    def y(I):
        I.two

    y.contract({"foo": string, "bar": list_of(string)})


# Parent base classes.


class Parent:
    @story
    def a(I):
        I.before
        I.x
        I.after


Parent.a.contract({"ham": integer, "eggs": integer, "beans": integer})


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


ParentWithSame.a.contract({"foo": integer, "bar": list_of(integer), "baz": integer})


class SequentialParent:
    @story
    def a(I):
        I.before
        I.x
        I.y
        I.after

    a.contract({})


class ParamParent:
    @story
    @arguments("ham", "eggs")
    def a(I):
        I.before
        I.x
        I.after


ParamParent.a.contract({"ham": integer, "eggs": integer, "beans": integer})


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
    {"foo": integer, "bar": list_of(integer), "baz": integer}
)


class ParamParentWithSameWithString:
    @story
    @arguments("foo", "bar")
    def a(I):
        I.before
        I.x
        I.after


ParamParentWithSameWithString.a.contract({"foo": string, "bar": list_of(string)})


# Root base classes.


class Root:
    @story
    def i(I):
        I.start
        I.a
        I.finish


Root.i.contract({"fizz": integer, "buzz": integer})


class RootWithSame:
    @story
    def i(I):
        I.start
        I.a
        I.finish


RootWithSame.i.contract({"foo": integer, "bar": list_of(integer), "baz": integer})


class SequentialRoot:
    @story
    def i(I):
        I.start
        I.a
        I.b
        I.finish


SequentialRoot.i.contract({"fizz": integer, "buzz": integer})


class ParamRoot:
    @story
    @arguments("fizz")
    def i(I):
        I.start
        I.a
        I.finish


ParamRoot.i.contract({"fizz": integer, "buzz": integer})
