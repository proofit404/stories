# -*- coding: utf-8 -*-
from typing import Dict
from typing import List

from pydantic import BaseModel

from stories import arguments
from stories import story
from stories.shortcuts import contract_in


# Constants.


representations = {
    "int_error": "value is not a valid integer",
    "list_of_int_error": "value is not a valid integer",
    "int_field_repr": "int",
    "str_field_repr": "str",
    "list_of_int_field_repr": "List[int]",
    "list_of_str_field_repr": "List[str]",
    "contract_class_repr": "<class 'pydantic.main.BaseModel'>",
}


# Child base classes.


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


class ChildWithShrink(object):
    @story
    def x(I):
        I.one

    @x.contract
    class Contract(BaseModel):
        baz: int


class ChildReuse(object):
    @story
    def x(I):
        I.one


class ChildAlias(object):
    @story
    def x(I):
        I.one

    @x.contract
    class Contract(BaseModel):
        foo: Dict[str, str]
        bar: Dict[str, str]
        baz: Dict[str, int]


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


class ParamChildAlias(object):
    @story
    @arguments("foo", "bar", "baz")
    def x(I):
        I.one

    @x.contract
    class Contract(BaseModel):
        foo: Dict[str, str]
        bar: Dict[str, str]
        baz: Dict[str, int]


# Next child base classes.


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
        I.two

    @y.contract
    class Contract(BaseModel):
        foo: str
        bar: List[str]


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


@ParentWithSame.a.contract
class Contract(BaseModel):  # noqa: F811
    foo: int
    bar: List[int]
    baz: int


class ParentReuse(object):
    @story
    def a(I):
        I.before
        I.x
        I.after


@ChildReuse.x.contract
@ParentReuse.a.contract
class Contract(BaseModel):  # noqa: F811
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


@ParamParent.a.contract
class Contract(BaseModel):  # noqa: F811
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


class ParamParentWithSame(object):
    @story
    @arguments("foo", "bar", "baz")
    def a(I):
        I.before
        I.after


@ParamParentWithSame.a.contract
class Contract(BaseModel):  # noqa: F811
    foo: int
    bar: List[int]
    baz: int


class ParamParentWithSameWithString(object):
    @story
    @arguments("foo", "bar")
    def a(I):
        I.before
        I.x
        I.after


@ParamParentWithSameWithString.a.contract
class Contract(BaseModel):  # noqa: F811
    foo: str
    bar: List[str]


# Next parent base classes.


class NextParamParentReuse(object):
    @story
    @arguments("foo", "bar")
    def b(I):
        I.before
        I.y
        I.after


@NextParamChildReuse.y.contract
@NextParamParentReuse.b.contract
class Contract(BaseModel):  # noqa: F811
    foo: int
    bar: List[int]
    baz: int


# Root base classes.


class Root(object):
    @story
    def i(I):
        I.start
        I.a
        I.finish


@contract_in(Root)
class Contract(BaseModel):  # noqa: F811
    fizz: int
    buzz: int


class RootWithSame(object):
    @story
    def i(I):
        I.start
        I.a
        I.finish


@contract_in(RootWithSame)
class Contract(BaseModel):  # noqa: F811
    foo: int
    bar: List[int]
    baz: int


class SequentialRoot(object):
    @story
    def i(I):
        I.start
        I.a
        I.b
        I.finish


@contract_in(SequentialRoot)
class Contract(BaseModel):  # noqa: F811
    fizz: int
    buzz: int


class ParamRoot(object):
    @story
    @arguments("fizz")
    def i(I):
        I.start
        I.a
        I.finish


@contract_in(ParamRoot)
class Contract(BaseModel):  # noqa: F811
    fizz: int
    buzz: int
