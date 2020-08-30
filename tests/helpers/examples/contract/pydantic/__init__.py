from typing import Dict
from typing import List

from pydantic import BaseModel

from stories import arguments
from stories import story


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


class Child:
    @story
    def x(I):
        I.one

    @x.contract
    class Contract(BaseModel):
        foo: int
        bar: List[int]
        baz: int


class ChildWithNull:
    @story
    def x(I):
        I.one


class ChildWithShrink:
    @story
    def x(I):
        I.one

    @x.contract
    class Contract(BaseModel):
        baz: int


class ChildAlias:
    @story
    def x(I):
        I.one

    @x.contract
    class Contract(BaseModel):
        foo: Dict[str, str]
        bar: Dict[str, str]
        baz: Dict[str, int]


class ParamChild:
    @story
    @arguments("foo", "bar")
    def x(I):
        I.one

    @x.contract
    class Contract(BaseModel):
        foo: int
        bar: List[int]
        baz: int


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
    class Contract(BaseModel):
        baz: int


class ParamChildAlias:
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


class NextChildWithSame:
    @story
    def y(I):
        I.one

    @y.contract
    class Contract(BaseModel):
        foo: int
        bar: List[int]
        baz: int


class NextParamChildWithString:
    @story
    @arguments("foo", "bar")
    def y(I):
        I.two

    @y.contract
    class Contract(BaseModel):
        foo: str
        bar: List[str]


# Parent base classes.


class Parent:
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
class Contract(BaseModel):  # noqa: F811
    foo: int
    bar: List[int]
    baz: int


class SequentialParent:
    @story
    def a(I):
        I.before
        I.x
        I.y
        I.after

    @a.contract
    class Contract(BaseModel):
        pass


class ParamParent:
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
class Contract(BaseModel):  # noqa: F811
    foo: int
    bar: List[int]
    baz: int


class ParamParentWithSameWithString:
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


# Root base classes.


class Root:
    @story
    def i(I):
        I.start
        I.a
        I.finish


@Root.i.contract
class Contract(BaseModel):  # noqa: F811
    fizz: int
    buzz: int


class RootWithSame:
    @story
    def i(I):
        I.start
        I.a
        I.finish


@RootWithSame.i.contract
class Contract(BaseModel):  # noqa: F811
    foo: int
    bar: List[int]
    baz: int


class SequentialRoot:
    @story
    def i(I):
        I.start
        I.a
        I.b
        I.finish


@SequentialRoot.i.contract
class Contract(BaseModel):  # noqa: F811
    fizz: int
    buzz: int


class ParamRoot:
    @story
    @arguments("fizz")
    def i(I):
        I.start
        I.a
        I.finish


@ParamRoot.i.contract
class Contract(BaseModel):  # noqa: F811
    fizz: int
    buzz: int
