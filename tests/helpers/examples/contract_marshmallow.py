from marshmallow import fields
from marshmallow import Schema
from marshmallow import utils

from stories import arguments
from stories import story
from stories import Success
from stories.shortcuts import contract_in


# We don't want to convert strings to unicode on Python 2.
utils.text_type = str


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


class ChildReuse(object):
    @story
    def x(I):
        I.one


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


@ParentWithSame.a.contract  # noqa: F811
class Contract(Schema):
    foo = fields.Integer()
    bar = fields.List(fields.Integer())
    baz = fields.Integer()


class ParentReuse(object):
    @story
    def a(I):
        I.before
        I.x
        I.after


@ChildReuse.x.contract  # noqa: F811
@ParentReuse.a.contract
class Contract(Schema):
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


@ParamParent.a.contract  # noqa: F811
class Contract(Schema):
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


@ParamParentWithSame.a.contract  # noqa: F811
class Contract(Schema):
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


@ParamParentWithSameWithString.a.contract  # noqa: F811
class Contract(Schema):
    foo = fields.String()
    bar = fields.List(fields.String())


# Next parent base classes.


class NextParamParentReuse(object):
    @story
    @arguments("foo", "bar")
    def b(I):
        I.before
        I.y
        I.after


@NextParamChildReuse.y.contract  # noqa: F811
@NextParamParentReuse.b.contract
class Contract(Schema):
    foo = fields.Integer()
    bar = fields.List(fields.Integer())
    baz = fields.Integer()


# Root base classes.


class Root(object):
    @story
    def i(I):
        I.start
        I.a
        I.finish


@contract_in(Root)  # noqa: F811
class Contract(Schema):
    fizz = fields.Integer()
    buzz = fields.Integer()


class RootWithSame(object):
    @story
    def i(I):
        I.start
        I.a
        I.finish


@contract_in(RootWithSame)  # noqa: F811
class Contract(Schema):
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


@contract_in(SequentialRoot)  # noqa: F811
class Contract(Schema):
    fizz = fields.Integer()
    buzz = fields.Integer()


class ParamRoot(object):
    @story
    @arguments("fizz")
    def i(I):
        I.start
        I.a
        I.finish


@contract_in(ParamRoot)  # noqa: F811
class Contract(Schema):
    fizz = fields.Integer()
    buzz = fields.Integer()
