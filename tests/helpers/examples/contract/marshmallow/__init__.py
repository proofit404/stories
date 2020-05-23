from marshmallow import fields
from marshmallow import Schema

from stories import arguments
from stories import story


# Constants.


representations = {
    "int_error": "Not b1 valid integer.",
    "list_of_int_error": """0:
    Not b1 valid integer.
    """.strip(),
    "int_field_repr": "Integer",
    "str_field_repr": "String",
    "list_of_int_field_repr": "List",
    "list_of_str_field_repr": "List",  # FIXME: Should show child schema.
    "contract_class_repr": "<class 'marshmallow.schema.Schema'>",
}


# Child base classes.


class Child:
    @story
    def a1(I):
        I.a1s1

    @a1.contract
    class Contract(Schema):
        a1v1 = fields.Integer()
        a1v2 = fields.List(fields.Integer())
        a1v3 = fields.Integer()


class ChildWithNull:
    @story
    def a1(I):
        I.a1s1


class ChildWithShrink:
    @story
    def a1(I):
        I.a1s1

    @a1.contract
    class Contract(Schema):
        a1v3 = fields.Integer()


class ChildAlias:
    @story
    def a1(I):
        I.a1s1

    @a1.contract
    class Contract(Schema):
        class _DictOfStr(Schema):
            key = fields.Str()

        class _DictOfInteger(Schema):
            key = fields.Integer()

        a1v1 = fields.Nested(_DictOfStr)
        a1v2 = fields.Nested(_DictOfStr)
        a1v3 = fields.Nested(_DictOfInteger)


class ParamChild:
    @story
    @arguments("a1v1", "a1v2")
    def a1(I):
        I.a1s1

    @a1.contract
    class Contract(Schema):
        a1v1 = fields.Integer()
        a1v2 = fields.List(fields.Integer())
        a1v3 = fields.Integer()


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

    @a1.contract
    class Contract(Schema):
        a1v3 = fields.Integer()


class ParamChildAlias:
    @story
    @arguments("a1v1", "a1v2", "a1v3")
    def a1(I):
        I.a1s1

    @a1.contract
    class Contract(Schema):
        class _DictOfStr(Schema):
            key = fields.Str()

        class _DictOfInteger(Schema):
            key = fields.Integer()

        a1v1 = fields.Nested(_DictOfStr)
        a1v2 = fields.Nested(_DictOfStr)
        a1v3 = fields.Nested(_DictOfInteger)


# Next child base classes.


class NextChildWithSame:
    @story
    def a2(I):
        I.a1s1

    @a2.contract
    class Contract(Schema):
        a1v1 = fields.Integer()
        a1v2 = fields.List(fields.Integer())
        a1v3 = fields.Integer()


class NextParamChildWithString:
    @story
    @arguments("a1v1", "a1v2")
    def a2(I):
        I.a2s1

    @a2.contract
    class Contract(Schema):
        a1v1 = fields.String()
        a1v2 = fields.List(fields.String())


# Parent base classes.


class Parent:
    @story
    def b1(I):
        I.b1s1
        I.a1
        I.b1s2


@Parent.b1.contract
class Contract(Schema):
    b1v1 = fields.Integer()
    b1v2 = fields.Integer()
    b1v3 = fields.Integer()


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


@ParentWithSame.b1.contract
class Contract(Schema):  # noqa: F811
    a1v1 = fields.Integer()
    a1v2 = fields.List(fields.Integer())
    a1v3 = fields.Integer()


class SequentialParent:
    @story
    def b1(I):
        I.b1s1
        I.a1
        I.a2
        I.b1s2

    @b1.contract  # FIXME: Should be inferred.
    class Contract(Schema):
        pass


class ParamParent:
    @story
    @arguments("b1v1", "b1v2")
    def b1(I):
        I.b1s1
        I.a1
        I.b1s2


@ParamParent.b1.contract
class Contract(Schema):  # noqa: F811
    b1v1 = fields.Integer()
    b1v2 = fields.Integer()
    b1v3 = fields.Integer()


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


@ParamParentWithSame.b1.contract
class Contract(Schema):  # noqa: F811
    a1v1 = fields.Integer()
    a1v2 = fields.List(fields.Integer())
    a1v3 = fields.Integer()


class ParamParentWithSameWithString:
    @story
    @arguments("a1v1", "a1v2")
    def b1(I):
        I.b1s1
        I.a1
        I.b1s2


@ParamParentWithSameWithString.b1.contract
class Contract(Schema):  # noqa: F811
    a1v1 = fields.String()
    a1v2 = fields.List(fields.String())


# Root base classes.


class Root:
    @story
    def c1(I):
        I.c1s1
        I.b1
        I.c1s2


@Root.c1.contract
class Contract(Schema):  # noqa: F811
    c1v1 = fields.Integer()
    c1v2 = fields.Integer()


class RootWithSame:
    @story
    def c1(I):
        I.c1s1
        I.b1
        I.c1s2


@RootWithSame.c1.contract
class Contract(Schema):  # noqa: F811
    a1v1 = fields.Integer()
    a1v2 = fields.List(fields.Integer())
    a1v3 = fields.Integer()


class SequentialRoot:
    @story
    def c1(I):
        I.c1s1
        I.b1
        I.b2
        I.c1s2


@SequentialRoot.c1.contract
class Contract(Schema):  # noqa: F811
    c1v1 = fields.Integer()
    c1v2 = fields.Integer()


class ParamRoot:
    @story
    @arguments("c1v1")
    def c1(I):
        I.c1s1
        I.b1
        I.c1s2


@ParamRoot.c1.contract
class Contract(Schema):  # noqa: F811
    c1v1 = fields.Integer()
    c1v2 = fields.Integer()
