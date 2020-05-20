# -*- coding: utf-8 -*-
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


class Child(object):
    @story
    def x(I):
        I.one

    @x.contract
    class Contract(Schema):
        foo = fields.Integer()
        bar = fields.List(fields.Integer())
        baz = fields.Integer()


class ChildWithNull(object):
    @story
    def x(I):
        I.one


class ChildWithShrink(object):
    @story
    def x(I):
        I.one

    @x.contract
    class Contract(Schema):
        baz = fields.Integer()


class ChildAlias(object):
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


class ParamChild(object):
    @story
    @arguments("foo", "bar")
    def x(I):
        I.one

    @x.contract
    class Contract(Schema):
        foo = fields.Integer()
        bar = fields.List(fields.Integer())
        baz = fields.Integer()


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

    @x.contract
    class Contract(Schema):
        baz = fields.Integer()


class ParamChildAlias(object):
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


class NextChildWithSame(object):
    @story
    def y(I):
        I.one

    @y.contract
    class Contract(Schema):
        foo = fields.Integer()
        bar = fields.List(fields.Integer())
        baz = fields.Integer()


class NextParamChildWithString(object):
    @story
    @arguments("foo", "bar")
    def y(I):
        I.two

    @y.contract
    class Contract(Schema):
        foo = fields.String()
        bar = fields.List(fields.String())


# Parent base classes.


class Parent(object):
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


@ParentWithSame.a.contract
class Contract(Schema):  # noqa: F811
    foo = fields.Integer()
    bar = fields.List(fields.Integer())
    baz = fields.Integer()


class SequentialParent(object):
    @story
    def a(I):
        I.before
        I.x
        I.y
        I.after

    @a.contract  # FIXME: Should be inferred.
    class Contract(Schema):
        pass


class ParamParent(object):
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


@ParamParentWithSame.a.contract
class Contract(Schema):  # noqa: F811
    foo = fields.Integer()
    bar = fields.List(fields.Integer())
    baz = fields.Integer()


class ParamParentWithSameWithString(object):
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


class Root(object):
    @story
    def i(I):
        I.start
        I.a
        I.finish


@Root.i.contract
class Contract(Schema):  # noqa: F811
    fizz = fields.Integer()
    buzz = fields.Integer()


class RootWithSame(object):
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


class SequentialRoot(object):
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


class ParamRoot(object):
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
