from typing import List

from pydantic import BaseModel

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

    @x.contract
    class Contract(BaseModel):
        foo: int
        bar: List[int]
        baz: int


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

    @x.contract
    class Contract(BaseModel):
        foo: int
        bar: List[int]
        baz: int


class NextChildWithSame(object):
    @story
    def y(I):
        I.one

    @y.contract
    class Contract(BaseModel):
        foo: int
        bar: List[int]
        baz: int


class NextParamChildWithString(object):
    @story
    @arguments("foo", "bar")
    def y(I):
        I.one

    @y.contract
    class Contract(BaseModel):
        foo: str
        bar: List[str]


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
    class Contract(BaseModel):
        baz: int


# Parent base classes.


class Parent(object):
    @story
    def a(I):
        I.before
        I.x
        I.after


@Parent.a.contract
class Contract(BaseModel):
    ham: int
    eggs: int
    beans: int


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
class Contract(BaseModel):
    foo: int
    bar: List[int]
    baz: int


class ParentReuse(object):
    @story
    def a(I):
        I.before
        I.x
        I.after


@ChildReuse.x.contract  # noqa: F811
@ParentReuse.a.contract
class Contract(BaseModel):
    foo: int
    bar: List[int]
    baz: int


class SequentialParent(object):
    @story
    def a(I):
        I.before
        I.x
        I.y
        I.after

    @a.contract
    class Contract(BaseModel):
        pass


class ParamParent(object):
    @story
    @arguments("ham", "eggs")
    def a(I):
        I.before
        I.x
        I.after


@ParamParent.a.contract  # noqa: F811
class Contract(BaseModel):
    ham: int
    eggs: int
    beans: int


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


@ParamParentWithSameWithString.a.contract  # noqa: F811
class Contract(BaseModel):
    foo: str
    bar: List[str]


# Root base classes.


class Root(object):
    @story
    def i(I):
        I.start
        I.a
        I.finish


@contract_in(Root)  # noqa: F811
class Contract(BaseModel):
    fizz: int
    buzz: int


class RootWithSame(object):
    @story
    def i(I):
        I.start
        I.a
        I.finish


@contract_in(RootWithSame)  # noqa: F811
class Contract(BaseModel):
    foo: int
    bar: List[int]
    baz: int


class ParamRoot(object):
    @story
    @arguments("fizz")
    def i(I):
        I.start
        I.a
        I.finish


@contract_in(ParamRoot)  # noqa: F811
class Contract(BaseModel):
    fizz: int
    buzz: int
