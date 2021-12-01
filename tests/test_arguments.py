"""Tests related to story arguments."""
import pytest

from stories import Argument
from stories import I
from stories import State
from stories import Story


@pytest.mark.parametrize("value", [1, "x", None])
def test_no_validation(r, m, value):
    """Argument allow passed state argument to be any value."""

    class A1(Story):
        I.a1s1
        I.a1s2
        I.a1s3

        a1s1 = m._normal_method
        a1s2 = m._assert_method("a1v1", value)
        a1s3 = m._normal_method

    class A1State(State):
        a1v1 = Argument()

    class B1(Story):
        I.b1s1
        I.a1
        I.b1s2

        b1s1 = m._assert_method("b1v1", value)
        b1s2 = m._normal_method

        def __init__(self):
            self.a1 = A1()

    class B1State(State):
        b1v1 = Argument()

    class C1(Story):
        I.c1s1
        I.b1
        I.c1s2

        c1s1 = m._assert_method("c1v1", value)
        c1s2 = m._normal_method

        def __init__(self):
            self.b1 = B1()

    class C1State(State):
        c1v1 = Argument()

    # First level.

    story = A1()
    state = A1State(a1v1=value)
    r.run(story, state)
    assert state.a1v1 == value

    # Second level.

    story = B1()
    state_class = B1State & A1State
    state = state_class(b1v1=value, a1v1=value)
    r.run(story, state)
    assert state.b1v1 == value

    # Third level.

    story = C1()
    state_class = C1State & B1State & A1State
    state = state_class(c1v1=value, b1v1=value, a1v1=value)
    r.run(story, state)
    assert state.c1v1 == value
