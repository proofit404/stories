from typing import Dict
from typing import List

from pydantic import BaseModel

from stories import arguments
from stories import story


# Constants.


representations = {
    "int_error": "value is not b1 valid integer",
    "list_of_int_error": "value is not b1 valid integer",
    "int_field_repr": "int",
    "str_field_repr": "str",
    "list_of_int_field_repr": "List[int]",
    "list_of_str_field_repr": "List[str]",
    "contract_class_repr": "<class 'pydantic.main.BaseModel'>",
}


# Child base classes.


class Child:
    @story
    def a1(I):
        I.a1s1

    @a1.contract
    class Contract(BaseModel):
        a1v1: int
        a1v2: List[int]
        a1v3: int


class ChildWithNull:
    @story
    def a1(I):
        I.a1s1


class ChildWithShrink:
    @story
    def a1(I):
        I.a1s1

    @a1.contract
    class Contract(BaseModel):
        a1v3: int


class ChildAlias:
    @story
    def a1(I):
        I.a1s1

    @a1.contract
    class Contract(BaseModel):
        a1v1: Dict[str, str]
        a1v2: Dict[str, str]
        a1v3: Dict[str, int]


class ParamChild:
    @story
    @arguments("a1v1", "a1v2")
    def a1(I):
        I.a1s1

    @a1.contract
    class Contract(BaseModel):
        a1v1: int
        a1v2: List[int]
        a1v3: int


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
    class Contract(BaseModel):
        a1v3: int


class ParamChildAlias:
    @story
    @arguments("a1v1", "a1v2", "a1v3")
    def a1(I):
        I.a1s1

    @a1.contract
    class Contract(BaseModel):
        a1v1: Dict[str, str]
        a1v2: Dict[str, str]
        a1v3: Dict[str, int]


# Next child base classes.


class NextChildWithSame:
    @story
    def a2(I):
        I.a1s1

    @a2.contract
    class Contract(BaseModel):
        a1v1: int
        a1v2: List[int]
        a1v3: int


class NextParamChildWithString:
    @story
    @arguments("a1v1", "a1v2")
    def a2(I):
        I.a2s1

    @a2.contract
    class Contract(BaseModel):
        a1v1: str
        a1v2: List[str]


# Parent base classes.


class Parent:
    @story
    def b1(I):
        I.b1s1
        I.a1
        I.b1s2


@Parent.b1.contract
class Contract(BaseModel):
    b1v1: int
    b1v2: int
    b1v3: int


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
class Contract(BaseModel):  # noqa: F811
    a1v1: int
    a1v2: List[int]
    a1v3: int


class SequentialParent:
    @story
    def b1(I):
        I.b1s1
        I.a1
        I.a2
        I.b1s2

    @b1.contract
    class Contract(BaseModel):
        pass


class ParamParent:
    @story
    @arguments("b1v1", "b1v2")
    def b1(I):
        I.b1s1
        I.a1
        I.b1s2


@ParamParent.b1.contract
class Contract(BaseModel):  # noqa: F811
    b1v1: int
    b1v2: int
    b1v3: int


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
class Contract(BaseModel):  # noqa: F811
    a1v1: int
    a1v2: List[int]
    a1v3: int


class ParamParentWithSameWithString:
    @story
    @arguments("a1v1", "a1v2")
    def b1(I):
        I.b1s1
        I.a1
        I.b1s2


@ParamParentWithSameWithString.b1.contract
class Contract(BaseModel):  # noqa: F811
    a1v1: str
    a1v2: List[str]


# Root base classes.


class Root:
    @story
    def c1(I):
        I.c1s1
        I.b1
        I.c1s2


@Root.c1.contract
class Contract(BaseModel):  # noqa: F811
    c1v1: int
    c1v2: int


class RootWithSame:
    @story
    def c1(I):
        I.c1s1
        I.b1
        I.c1s2


@RootWithSame.c1.contract
class Contract(BaseModel):  # noqa: F811
    a1v1: int
    a1v2: List[int]
    a1v3: int


class SequentialRoot:
    @story
    def c1(I):
        I.c1s1
        I.b1
        I.b2
        I.c1s2


@SequentialRoot.c1.contract
class Contract(BaseModel):  # noqa: F811
    c1v1: int
    c1v2: int


class ParamRoot:
    @story
    @arguments("c1v1")
    def c1(I):
        I.c1s1
        I.b1
        I.c1s2


@ParamRoot.c1.contract
class Contract(BaseModel):  # noqa: F811
    c1v1: int
    c1v2: int
