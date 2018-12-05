# TODO:
#
# [ ] Check incoming reasons type in the StoryFactory.
#
# [ ] Story and substory protocol mismatch.
#
# [ ] Substory can not use failures from the protocol superset of the
#     parent story.
from enum import Enum

from stories import Failure, StoryFactory, Success, story


story_with_list = StoryFactory(failures=["foo", "bar", "baz"])


Errors = Enum("Errors", "foo bar baz")
story_with_enum = StoryFactory(failures=Errors)


# Simple story.


class CommonSimple(object):

    # Wrong reason.

    def two(self, ctx):
        return Failure("'foo' is too big")

    # Null reason.

    def three(self, ctx):
        return Failure()


class SimpleWithList(CommonSimple):
    @story_with_list
    def x(I):
        I.one

    @story_with_list
    def y(I):
        I.two

    @story_with_list
    def z(I):
        I.three

    def one(self, ctx):
        return Failure("foo")


class SimpleWithEnum(CommonSimple):
    @story_with_enum
    def x(I):
        I.one

    @story_with_enum
    def y(I):
        I.two

    @story_with_enum
    def z(I):
        I.three

    def one(self, ctx):
        return Failure(Errors.foo)


# Substory in the same class.


class CommonSubstory(object):
    def before(self, ctx):
        return Success()

    def after(self, ctx):
        return Success()


class SimpleSubstoryWithList(CommonSubstory, SimpleWithList):
    @story_with_list
    def a(I):
        I.before
        I.x
        I.after

    @story_with_list
    def b(I):
        I.before
        I.y
        I.after

    @story_with_list
    def c(I):
        I.before
        I.z
        I.after


class SimpleSubstoryWithEnum(CommonSubstory, SimpleWithEnum):
    @story_with_enum
    def a(I):
        I.before
        I.x
        I.after

    @story_with_enum
    def b(I):
        I.before
        I.y
        I.after

    @story_with_enum
    def c(I):
        I.before
        I.z
        I.after


# Dependency injection of the substory.


class SubstoryDIWithList(CommonSubstory):
    def __init__(self):
        self.x = SimpleWithList().x
        self.y = SimpleWithList().y
        self.z = SimpleWithList().z

    @story_with_list
    def a(I):
        I.before
        I.x
        I.after

    @story_with_list
    def b(I):
        I.before
        I.y
        I.after

    @story_with_list
    def c(I):
        I.before
        I.z
        I.after


class SubstoryDIWithEnum(CommonSubstory):
    def __init__(self):
        self.x = SimpleWithEnum().x
        self.y = SimpleWithEnum().y
        self.z = SimpleWithEnum().z

    @story_with_enum
    def a(I):
        I.before
        I.x
        I.after

    @story_with_enum
    def b(I):
        I.before
        I.y
        I.after

    @story_with_enum
    def c(I):
        I.before
        I.z
        I.after


# Reason used without protocol definition.


class ReasonWithSimple(CommonSimple):
    @story
    def y(I):
        I.two


class ReasonWithSimpleSubstory(CommonSubstory, ReasonWithSimple):
    @story
    def b(I):
        I.before
        I.y
        I.after


class ReasonWithSubstoryDI(CommonSubstory):
    def __init__(self):
        self.y = ReasonWithSimple().y

    @story
    def b(I):
        I.before
        I.y
        I.after
