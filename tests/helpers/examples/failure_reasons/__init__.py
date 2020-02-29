# -*- coding: utf-8 -*-
from enum import Enum

from stories import story
from stories.shortcuts import failures_in


# Base classes.


class ChildWithNull(object):
    @story
    def x(I):
        I.one


class NextChildWithNull(object):
    @story
    def y(I):
        I.two


class ParentWithNull(object):
    @story
    def a(I):
        I.before
        I.x
        I.after


class SequenceParentWithNull(object):
    @story
    def a(I):
        I.before
        I.x
        I.y
        I.after


class ChildWithList(object):
    @story
    def x(I):
        I.one


ChildWithList.x.failures(["foo", "bar", "baz"])


class NextChildWithList(object):
    @story
    def y(I):
        I.two


NextChildWithList.y.failures(["spam", "ham", "eggs"])


class ParentWithList(object):
    @story
    def a(I):
        I.before
        I.x
        I.after


failures_in(ParentWithList, ["foo", "bar", "baz"])


class WideParentWithList(object):
    @story
    def a(I):
        I.before
        I.x
        I.after


failures_in(WideParentWithList, ["foo", "bar", "baz", "quiz"])


class ShrinkParentWithList(object):
    @story
    def a(I):
        I.before
        I.x
        I.after


failures_in(ShrinkParentWithList, ["foo", "quiz"])


class ChildWithEnum(object):
    @story
    def x(I):
        I.one

    @x.failures
    class Errors(Enum):
        foo = 1
        bar = 2
        baz = 3


class NextChildWithEnum(object):
    @story
    def y(I):
        I.two

    @y.failures
    class Errors(Enum):
        spam = 1
        ham = 2
        eggs = 3


class ParentWithEnum(object):
    @story
    def a(I):
        I.before
        I.x
        I.after


@failures_in(ParentWithEnum)
class Errors(Enum):
    foo = 1
    bar = 2
    baz = 3


class WideParentWithEnum(object):
    @story
    def a(I):
        I.before
        I.x
        I.after


@failures_in(WideParentWithEnum)
class Errors(Enum):  # noqa: F811
    foo = 1
    bar = 2
    baz = 3
    quiz = 4


class ShrinkParentWithEnum(object):
    @story
    def a(I):
        I.before
        I.x
        I.after


@failures_in(ShrinkParentWithEnum)
class Errors(Enum):  # noqa: F811
    foo = 1
    quiz = 4
