"""Tests related to user friendly representations."""
from stories import State
from stories import Union
from stories import Variable
from validators import _equal_to


def test_variable_representation():
    """Variable should show validator."""
    assert repr(Variable()) == "Variable()"
    assert repr(Variable(_equal_to(1))) == "Variable(_equal_to(1))"


def test_union_representation():
    """State union should show variables."""

    class A1State(State):
        a1v1 = Variable(_equal_to(0))

    class B1State(State):
        b1v1 = Variable(_equal_to(1))

    state_class = Union(B1State, A1State)
    expected = """
Union(B1State, A1State):
    a1v1 = Variable(_equal_to(0))
    b1v1 = Variable(_equal_to(1))
    """.strip()
    assert repr(state_class) == expected
