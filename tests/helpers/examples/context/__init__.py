# -*- coding: utf-8 -*-
from stories import arguments
from stories import story


# Base classes.


class Child(object):
    @story
    def x(I):
        I.one


class ParamChild(object):
    @story
    @arguments("bar")
    def x(I):
        I.one


class Parent(object):
    @story
    def a(I):
        I.before
        I.x
        I.after


class ParamParent(object):
    @story
    @arguments("bar")
    def a(I):
        I.before
        I.x
        I.after
