from enum import Enum

from stories import story


# Base classes.


class ChildWithNull:
    @story
    def x(I):
        I.one


class NextChildWithNull:
    @story
    def y(I):
        I.two


class ParentWithNull:
    @story
    def a(I):
        I.before
        I.x
        I.after


class SequenceParentWithNull:
    @story
    def a(I):
        I.before
        I.x
        I.y
        I.after


class ChildWithList:
    @story
    def x(I):
        I.one


ChildWithList.x.failures(["foo", "bar", "baz"])


class NextChildWithList:
    @story
    def y(I):
        I.two


NextChildWithList.y.failures(["spam", "ham", "eggs"])


class ParentWithList:
    @story
    def a(I):
        I.before
        I.x
        I.after


ParentWithList.a.failures(["foo", "bar", "baz"])


class WideParentWithList:
    @story
    def a(I):
        I.before
        I.x
        I.after


WideParentWithList.a.failures(["foo", "bar", "baz", "quiz"])


class ShrinkParentWithList:
    @story
    def a(I):
        I.before
        I.x
        I.after


ShrinkParentWithList.a.failures(["foo", "quiz"])


class ChildWithEnum:
    @story
    def x(I):
        I.one

    @x.failures
    class Errors(Enum):
        foo = 1
        bar = 2
        baz = 3


class NextChildWithEnum:
    @story
    def y(I):
        I.two

    @y.failures
    class Errors(Enum):
        spam = 1
        ham = 2
        eggs = 3


class ParentWithEnum:
    @story
    def a(I):
        I.before
        I.x
        I.after


@ParentWithEnum.a.failures
class Errors(Enum):
    foo = 1
    bar = 2
    baz = 3


class WideParentWithEnum:
    @story
    def a(I):
        I.before
        I.x
        I.after


@WideParentWithEnum.a.failures
class Errors(Enum):  # noqa: F811
    foo = 1
    bar = 2
    baz = 3
    quiz = 4


class ShrinkParentWithEnum:
    @story
    def a(I):
        I.before
        I.x
        I.after


@ShrinkParentWithEnum.a.failures
class Errors(Enum):  # noqa: F811
    foo = 1
    quiz = 4
