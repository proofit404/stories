from marshmallow import fields
from marshmallow import Schema

from stories import arguments
from stories import story


# Constants.


representations = {
    "int_error": "Not a valid integer.",
    "list_of_int_error": """0:
    Not a valid integer.
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
    def x(I):
        I.one

    @x.contract
    class Contract(Schema):
        foo = fields.Integer()
        bar = fields.List(fields.Integer())
        baz = fields.Integer()


class ChildWithNull:
    @story
    def x(I):
        I.one


class ChildWithShrink:
    @story
    def x(I):
        I.one

    @x.contract
    class Contract(Schema):
        baz = fields.Integer()


class ChildAlias:
    @story
    def x(I):
        I.one

    @x.contract
    class Contract(Schema):
        class _DictOfStr(Schema):
            key = fields.Str()

        class _DictOfInteger(Schema):
            key = fields.Integer()

        foo = fields.Nested(_DictOfStr)
        bar = fields.Nested(_DictOfStr)
        baz = fields.Nested(_DictOfInteger)


class ParamChild:
    @story
    @arguments("foo", "bar")
    def x(I):
        I.one

    @x.contract
    class Contract(Schema):
        foo = fields.Integer()
        bar = fields.List(fields.Integer())
        baz = fields.Integer()


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

    @x.contract
    class Contract(Schema):
        baz = fields.Integer()


class ParamChildAlias:
    @story
    @arguments("foo", "bar", "baz")
    def x(I):
        I.one

    @x.contract
    class Contract(Schema):
        class _DictOfStr(Schema):
            key = fields.Str()

        class _DictOfInteger(Schema):
            key = fields.Integer()

        foo = fields.Nested(_DictOfStr)
        bar = fields.Nested(_DictOfStr)
        baz = fields.Nested(_DictOfInteger)


# Next child base classes.


class NextChildWithSame:
    @story
    def y(I):
        I.one

    @y.contract
    class Contract(Schema):
        foo = fields.Integer()
        bar = fields.List(fields.Integer())
        baz = fields.Integer()


class NextParamChildWithString:
    @story
    @arguments("foo", "bar")
    def y(I):
        I.two

    @y.contract
    class Contract(Schema):
        foo = fields.String()
        bar = fields.List(fields.String())


# Parent base classes.


class Parent:
    @story
    def a(I):
        I.before
        I.x
        I.after


@Parent.a.contract
class Contract(Schema):
    ham = fields.Integer()
    eggs = fields.Integer()
    beans = fields.Integer()


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


@ParentWithSame.a.contract
class Contract(Schema):  # noqa: F811
    foo = fields.Integer()
    bar = fields.List(fields.Integer())
    baz = fields.Integer()


class SequentialParent:
    @story
    def a(I):
        I.before
        I.x
        I.y
        I.after

    @a.contract  # FIXME: Should be inferred.
    class Contract(Schema):
        pass


class ParamParent:
    @story
    @arguments("ham", "eggs")
    def a(I):
        I.before
        I.x
        I.after


@ParamParent.a.contract
class Contract(Schema):  # noqa: F811
    ham = fields.Integer()
    eggs = fields.Integer()
    beans = fields.Integer()


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


@ParamParentWithSame.a.contract
class Contract(Schema):  # noqa: F811
    foo = fields.Integer()
    bar = fields.List(fields.Integer())
    baz = fields.Integer()


class ParamParentWithSameWithString:
    @story
    @arguments("foo", "bar")
    def a(I):
        I.before
        I.x
        I.after


@ParamParentWithSameWithString.a.contract
class Contract(Schema):  # noqa: F811
    foo = fields.String()
    bar = fields.List(fields.String())


# Root base classes.


class Root:
    @story
    def i(I):
        I.start
        I.a
        I.finish


@Root.i.contract
class Contract(Schema):  # noqa: F811
    fizz = fields.Integer()
    buzz = fields.Integer()


class RootWithSame:
    @story
    def i(I):
        I.start
        I.a
        I.finish


@RootWithSame.i.contract
class Contract(Schema):  # noqa: F811
    foo = fields.Integer()
    bar = fields.List(fields.Integer())
    baz = fields.Integer()


class SequentialRoot:
    @story
    def i(I):
        I.start
        I.a
        I.b
        I.finish


@SequentialRoot.i.contract
class Contract(Schema):  # noqa: F811
    fizz = fields.Integer()
    buzz = fields.Integer()


class ParamRoot:
    @story
    @arguments("fizz")
    def i(I):
        I.start
        I.a
        I.finish


@ParamRoot.i.contract
class Contract(Schema):  # noqa: F811
    fizz = fields.Integer()
    buzz = fields.Integer()
