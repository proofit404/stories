"""Tests related to story arguments."""
import pytest

from stories import Argument
from stories import I
from stories import State
from stories import Story
from stories import Variable
from stories.exceptions import StateError


@pytest.mark.parametrize("value", [1, "x", None])
def test_no_validation(r, m, value):
    """Argument allow passed state argument to be any value."""

    class A1(Story):
        I.a1s1
        I.a1s2
        I.a1s3

        a1s1 = m._normal_method
        a1s2 = m._assert_method("a1a1", value)
        a1s3 = m._normal_method

    class A1State(State):
        a1a1 = Argument()

    class B1(Story):
        I.b1s1
        I.a1
        I.b1s2

        b1s1 = m._assert_method("b1a1", value)
        b1s2 = m._normal_method

        def __init__(self):
            self.a1 = A1()

    class B1State(State):
        b1a1 = Argument()

    class C1(Story):
        I.c1s1
        I.b1
        I.c1s2

        c1s1 = m._assert_method("c1a1", value)
        c1s2 = m._normal_method

        def __init__(self):
            self.b1 = B1()

    class C1State(State):
        c1a1 = Argument()

    # First level.

    story = A1()
    state = A1State(a1a1=value)
    r.run(story, state)
    assert state.a1a1 == value

    # Second level.

    story = B1()
    state_class = B1State & A1State
    state = state_class(b1a1=value, a1a1=value)
    r.run(story, state)
    assert state.b1a1 == value

    # Third level.

    story = C1()
    state_class = C1State & B1State & A1State
    state = state_class(c1a1=value, b1a1=value, a1a1=value)
    r.run(story, state)
    assert state.c1a1 == value


def test_unknown_argument(r, m):
    """Deny pass constructor arguments not defined by Argument."""

    class A1State(State):
        a1a1 = Argument()

    class B1State(State):
        b1a1 = Argument()

    class C1State(State):
        c1a1 = Argument()

    # First level.

    with pytest.raises(StateError) as exc_info:
        A1State(a1a2=1)
    assert (
        str(exc_info.value)
        == """
Unknown argument passed: a1a2

A1State
    """.strip()
    )

    # Second level.

    state_class = B1State & A1State
    with pytest.raises(StateError) as exc_info:
        state_class(b1a2=2)
    assert (
        str(exc_info.value)
        == """
Unknown argument passed: b1a2

B1State & A1State
    """.strip()
    )

    # Third level.

    state_class = C1State & B1State & A1State

    with pytest.raises(StateError) as exc_info:
        state_class(c1a2=3)
    assert (
        str(exc_info.value)
        == """
Unknown argument passed: c1a2

C1State & B1State & A1State
    """.strip()
    )


def test_variable_is_not_argument(r, m):
    """Deny pass constructor arguments even if it was declared by Variable."""

    class A1State(State):
        a1a1 = Argument()
        a1v2 = Variable()

    class B1State(State):
        b1a1 = Argument()
        b1v2 = Variable()

    class C1State(State):
        c1a1 = Argument()
        c1v2 = Variable()

    # First level.

    with pytest.raises(StateError) as exc_info:
        A1State(a1v2=1)
    assert (
        str(exc_info.value)
        == """
Unknown argument passed: a1v2

A1State
    """.strip()
    )

    # Second level.

    state_class = B1State & A1State
    with pytest.raises(StateError) as exc_info:
        state_class(b1v2=2)
    assert (
        str(exc_info.value)
        == """
Unknown argument passed: b1v2

B1State & A1State
    """.strip()
    )

    # Third level.

    state_class = C1State & B1State & A1State

    with pytest.raises(StateError) as exc_info:
        state_class(c1v2=3)
    assert (
        str(exc_info.value)
        == """
Unknown argument passed: c1v2

C1State & B1State & A1State
    """.strip()
    )
