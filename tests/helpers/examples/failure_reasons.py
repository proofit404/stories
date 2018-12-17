# TODO:
#
# [ ] Check incoming reasons type in the 'failures' story method.
#
# [ ] Substory can not use failures from the protocol superset of the
#     parent story.
#
# [ ] Protocol errors should be visible in the context representation.
#
# [ ] Expand parent and substory expand:
#
#     - Substory with empty result can not return failure if parent
#       story defines errors protocol

from enum import Enum

from stories import Failure, Success, story


# Mixins.


class CommonSimple(object):

    # Wrong reason.

    def two(self, ctx):
        return Failure("'foo' is too big")

    # Null reason.

    def three(self, ctx):
        return Failure()


class CommonSubstory(object):
    def before(self, ctx):
        return Success()

    def after(self, ctx):
        return Success()


# Arguments of the Failure class.


class SimpleWithList(CommonSimple):
    @story
    def x(I):
        I.one

    @story
    def y(I):
        I.two

    @story
    def z(I):
        I.three

    def one(self, ctx):
        return Failure("foo")

    errors = z.failures(y.failures(x.failures(["foo", "bar", "baz"])))


class SimpleWithEnum(CommonSimple):
    @story
    def x(I):
        I.one

    @story
    def y(I):
        I.two

    @story
    def z(I):
        I.three

    def one(self, ctx):
        return Failure(self.Errors.foo)

    @x.failures
    @y.failures
    @z.failures
    class Errors(Enum):
        foo = 1
        bar = 2
        baz = 3


class SimpleSubstoryWithList(CommonSubstory, SimpleWithList):
    @story
    def a(I):
        I.before
        I.x
        I.after

    @story
    def b(I):
        I.before
        I.y
        I.after

    @story
    def c(I):
        I.before
        I.z
        I.after

    errors = c.failures(b.failures(a.failures(["foo", "bar", "baz"])))


class SimpleSubstoryWithEnum(CommonSubstory, SimpleWithEnum):
    @story
    def a(I):
        I.before
        I.x
        I.after

    @story
    def b(I):
        I.before
        I.y
        I.after

    @story
    def c(I):
        I.before
        I.z
        I.after

    @a.failures
    @b.failures
    @c.failures
    class Errors(Enum):
        foo = 1
        bar = 2
        baz = 3


class SubstoryDIWithList(CommonSubstory):
    def __init__(self):
        self.x = SimpleWithList().x
        self.y = SimpleWithList().y
        self.z = SimpleWithList().z

    @story
    def a(I):
        I.before
        I.x
        I.after

    @story
    def b(I):
        I.before
        I.y
        I.after

    @story
    def c(I):
        I.before
        I.z
        I.after

    errors = c.failures(b.failures(a.failures(["foo", "bar", "baz"])))


class SubstoryDIWithEnum(CommonSubstory):
    def __init__(self):
        self.x = SimpleWithEnum().x
        self.y = SimpleWithEnum().y
        self.z = SimpleWithEnum().z

    @story
    def a(I):
        I.before
        I.x
        I.after

    @story
    def b(I):
        I.before
        I.y
        I.after

    @story
    def c(I):
        I.before
        I.z
        I.after

    @a.failures
    @b.failures
    @c.failures
    class Errors(Enum):
        foo = 1
        bar = 2
        baz = 3


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


# Arguments of the result class methods.


class SummaryWithSimple(CommonSimple):
    @story
    def z(I):
        I.three


class SummaryWithSimpleSubstory(CommonSubstory, SummaryWithSimple):
    @story
    def c(I):
        I.before
        I.z
        I.after


class SummaryWithSubstoryDI(CommonSubstory):
    def __init__(self):
        self.z = SummaryWithSimple().z

    @story
    def c(I):
        I.before
        I.z
        I.after


# Composition of the stories.


class EmptyMatch(object):
    @story
    def x(I):
        I.one

    def one(self, ctx):
        return Failure()


class SimpleMatchWithList(object):
    @story
    def x(I):
        I.one

    def one(self, ctx):
        return Failure("foo")

    errors = x.failures(["foo", "bar", "baz"])


class SimpleMatchWithEnum(object):
    @story
    def x(I):
        I.one

    def one(self, ctx):
        return Failure(self.Errors.foo)

    @x.failures
    class Errors(Enum):
        foo = 1
        bar = 2
        baz = 3


class EmptySubstoryMatch(EmptyMatch):
    @story
    def a(I):
        I.x


class SimpleSubstoryMatchWithList(SimpleMatchWithList):
    @story
    def a(I):
        I.x

    errors = a.failures(["foo", "bar", "baz", "quiz"])


class SimpleSubstoryMatchWithEnum(SimpleMatchWithEnum):
    @story
    def a(I):
        I.x

    @a.failures
    class Errors(Enum):
        foo = 1
        bar = 2
        baz = 3
        quiz = 4


class EmptyDIMatch(object):
    def __init__(self):
        self.x = EmptyMatch().x

    @story
    def a(I):
        I.x


class SubstoryDIMatchWithList(object):
    def __init__(self):
        self.x = SimpleMatchWithList().x

    @story
    def a(I):
        I.x

    errors = a.failures(["foo", "bar", "baz", "quiz"])


class SubstoryDIMatchWithEnum(object):
    def __init__(self):
        self.x = SimpleMatchWithEnum().x

    @story
    def a(I):
        I.x

    @a.failures
    class Errors(Enum):
        foo = 1
        bar = 2
        baz = 3
        quiz = 4


class EmptyMismatch(object):
    @story
    def x(I):
        pass


class ParentMismatch(object):
    @story
    def x(I):
        pass

    errors = x.failures(["foo", "quiz"])


class SimpleMismatchWithList(object):
    @story
    def x(I):
        pass

    errors = x.failures(["foo", "bar", "baz"])


class SimpleMismatchWithEnum(object):
    @story
    def x(I):
        pass

    @x.failures
    class Errors(Enum):
        foo = 1
        bar = 2
        baz = 3


class EmptySubstoryMismatch(EmptyMismatch):
    @story
    def a(I):
        I.x

    errors = a.failures(["foo", "quiz"])


class EmptyParentMismatch(ParentMismatch):
    @story
    def a(I):
        I.x


class SimpleSubstoryMismatchWithList(SimpleMismatchWithList):
    @story
    def a(I):
        I.x

    errors = a.failures(["foo", "quiz"])


class SimpleSubstoryMismatchWithEnum(SimpleMismatchWithEnum):
    @story
    def a(I):
        I.x

    @a.failures
    class Errors(Enum):
        foo = 1
        quiz = 2


class EmptyDIMismatch(object):
    def __init__(self):
        self.x = EmptyMismatch().x

    @story
    def a(I):
        I.x

    errors = a.failures(["foo", "quiz"])


class ParentDIMismatch(object):
    def __init__(self):
        self.x = ParentMismatch().x

    @story
    def a(I):
        I.x


class SubstoryDIMismatchWithList(object):
    def __init__(self):
        self.x = SimpleMismatchWithList().x

    @story
    def a(I):
        I.x

    errors = a.failures(["foo", "quiz"])


class SubstoryDIMismatchWithEnum(object):
    def __init__(self):
        self.x = SimpleMismatchWithEnum().x

    @story
    def a(I):
        I.x

    @a.failures
    class Errors(Enum):
        foo = 1
        quiz = 2
