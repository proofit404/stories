"""Tests related to story variables."""
from functools import reduce

import pytest

from stories import Argument
from stories import I
from stories import State
from stories import Story
from stories import Union
from stories import Variable
from stories.exceptions import StateError
from validators import _equal_to
from validators import _greater_than
from validators import _is_integer
from validators import _less_than
from validators import _ValidationError


@pytest.mark.parametrize("value", [1, "x", None])
@pytest.mark.parametrize("definition", [Variable, Argument])
def test_no_validation(r, m, value, definition):
    """Variable allow state attribute assignment to any value."""

    class A1(Story):
        I.a1s1
        I.a1s2
        I.a1s3

        a1s1 = m._normal_method
        a1s2 = m._assign_method("a1v1", value)
        a1s3 = m._normal_method

    class A1State(State):
        a1v1 = definition()

    class B1(Story):
        I.b1s1
        I.a1
        I.b1s2

        b1s1 = m._assign_method("b1v1", value)
        b1s2 = m._normal_method

        def __init__(self):
            self.a1 = A1()

    class B1State(State):
        b1v1 = definition()

    class C1(Story):
        I.c1s1
        I.b1
        I.c1s2

        c1s1 = m._assign_method("c1v1", value)
        c1s2 = m._normal_method

        def __init__(self):
            self.b1 = B1()

    class C1State(State):
        c1v1 = definition()

    # First level.

    story = A1()
    state = A1State()
    r.run(story, state)
    assert state.a1v1 == value

    # Second level.

    story = B1()
    state_class = Union(B1State, A1State)
    state = state_class()
    r.run(story, state)
    assert state.b1v1 == value

    # Third level.

    story = C1()
    state_class = Union(C1State, B1State, A1State)
    state = state_class()
    r.run(story, state)
    assert state.c1v1 == value


@pytest.mark.parametrize("definition", [Variable, Argument])
def test_unknown_variable(r, m, definition):
    """Deny attribute assignment not defined by Variable."""

    class A1(Story):
        I.a1s1
        I.a1s2
        I.a1s3

        a1s1 = m._normal_method
        a1s2 = m._assign_method("a1v2", 1)
        a1s3 = m._normal_method

    class A1State(State):
        a1v1 = definition()

    class B1(Story):
        I.b1s1
        I.a1
        I.b1s2

        b1s1 = m._assign_method("b1v2", 2)
        b1s2 = m._normal_method

        def __init__(self):
            self.a1 = A1()

    class B1State(State):
        b1v1 = definition()

    class C1(Story):
        I.c1s1
        I.b1
        I.c1s2

        c1s1 = m._assign_method("c1v2", 3)
        c1s2 = m._normal_method

        def __init__(self):
            self.b1 = B1()

    class C1State(State):
        c1v1 = definition()

    # First level.

    story = A1()
    state = A1State()
    with pytest.raises(StateError) as exc_info:
        r.run(story, state)
    assert (
        str(exc_info.value)
        == """
Unknown variable assignment: a1v2

A1State
    """.strip()
    )

    # Second level.

    story = B1()
    state_class = Union(B1State, A1State)
    state = state_class()
    with pytest.raises(StateError) as exc_info:
        r.run(story, state)
    assert (
        str(exc_info.value)
        == """
Unknown variable assignment: b1v2

Union(B1State, A1State)
    """.strip()
    )

    # Third level.

    story = C1()
    state_class = Union(C1State, B1State, A1State)
    state = state_class()
    with pytest.raises(StateError) as exc_info:
        r.run(story, state)
    assert (
        str(exc_info.value)
        == """
Unknown variable assignment: c1v2

Union(C1State, B1State, A1State)
    """.strip()
    )


@pytest.mark.parametrize("definition", [Variable, Argument])
def test_successful_validation(r, m, definition):
    """Variable runs validation on state attribute assignment."""

    class A1(Story):
        I.a1s1
        I.a1s2
        I.a1s3

        a1s1 = m._normal_method
        a1s2 = m._assign_method("a1v1", 1)
        a1s3 = m._normal_method

    class A1State(State):
        a1v1 = definition(_is_integer)

    class B1(Story):
        I.b1s1
        I.a1
        I.b1s2

        b1s1 = m._assign_method("b1v1", 2)
        b1s2 = m._normal_method

        def __init__(self):
            self.a1 = A1()

    class B1State(State):
        b1v1 = definition(_is_integer)

    class C1(Story):
        I.c1s1
        I.b1
        I.c1s2

        c1s1 = m._assign_method("c1v1", 3)
        c1s2 = m._normal_method

        def __init__(self):
            self.b1 = B1()

    class C1State(State):
        c1v1 = definition(_is_integer)

    # First level.

    story = A1()
    state = A1State()
    r.run(story, state)
    assert state.a1v1 == 1

    # Second level.

    story = B1()
    state_class = Union(B1State, A1State)
    state = state_class()
    r.run(story, state)
    assert state.b1v1 == 2

    # Third level.

    story = C1()
    state_class = Union(C1State, B1State, A1State)
    state = state_class()
    r.run(story, state)
    assert state.c1v1 == 3


@pytest.mark.parametrize("definition", [Variable, Argument])
def test_failed_validation(r, m, definition):
    """Validator function should raise an error."""

    class A1(Story):
        I.a1s1
        I.a1s2
        I.a1s3

        a1s1 = m._normal_method
        a1s2 = m._assign_method("a1v1", "foo")
        a1s3 = m._normal_method

    class A1State(State):
        a1v1 = definition(_is_integer)

    class B1(Story):
        I.b1s1
        I.a1
        I.b1s2

        b1s1 = m._assign_method("b1v1", "bar")
        b1s2 = m._normal_method

        def __init__(self):
            self.a1 = A1()

    class B1State(State):
        b1v1 = definition(_is_integer)

    class C1(Story):
        I.c1s1
        I.b1
        I.c1s2

        c1s1 = m._assign_method("c1v1", "baz")
        c1s2 = m._normal_method

        def __init__(self):
            self.b1 = B1()

    class C1State(State):
        c1v1 = definition(_is_integer)

    # First level.

    story = A1()
    state = A1State()
    with pytest.raises(_ValidationError) as exc_info:
        r.run(story, state)
    assert not hasattr(state, "a1v1")
    assert exc_info.value.args == ("foo",)

    # Second level.

    story = B1()
    state_class = Union(B1State, A1State)
    state = state_class()
    with pytest.raises(_ValidationError) as exc_info:
        r.run(story, state)
    assert not hasattr(state, "b1v1")
    assert exc_info.value.args == ("bar",)

    # Third level.

    story = C1()
    state_class = Union(C1State, B1State, A1State)
    state = state_class()
    with pytest.raises(_ValidationError) as exc_info:
        r.run(story, state)
    assert not hasattr(state, "c1v1")
    assert exc_info.value.args == ("baz",)


@pytest.mark.parametrize("definition", [Variable, Argument])
def test_value_normalization(r, m, definition):
    """Validator function should return normalized value."""

    class A1(Story):
        I.a1s1
        I.a1s2
        I.a1s3

        a1s1 = m._normal_method
        a1s2 = m._assign_method("a1v1", "1")
        a1s3 = m._normal_method

    class A1State(State):
        a1v1 = definition(_is_integer)

    class B1(Story):
        I.b1s1
        I.a1
        I.b1s2

        b1s1 = m._assign_method("b1v1", "2")
        b1s2 = m._normal_method

        def __init__(self):
            self.a1 = A1()

    class B1State(State):
        b1v1 = definition(_is_integer)

    class C1(Story):
        I.c1s1
        I.b1
        I.c1s2

        c1s1 = m._assign_method("c1v1", "3")
        c1s2 = m._normal_method

        def __init__(self):
            self.b1 = B1()

    class C1State(State):
        c1v1 = definition(_is_integer)

    # First level.

    story = A1()
    state = A1State()
    r.run(story, state)
    assert state.a1v1 == 1

    # Second level.

    story = B1()
    state_class = Union(B1State, A1State)
    state = state_class()
    r.run(story, state)
    assert state.b1v1 == 2

    # Third level.

    story = C1()
    state_class = Union(C1State, B1State, A1State)
    state = state_class()
    r.run(story, state)
    assert state.c1v1 == 3


@pytest.mark.parametrize("definition", [Variable, Argument])
def test_state_union_merge_validators_success(r, m, definition):
    """Validator functions in state union should be merged."""

    class A1(Story):
        I.a1s1
        I.a1s2
        I.a1s3

        a1s1 = m._normal_method
        a1s2 = m._assign_method("a1v1", 1)
        a1s3 = m._normal_method

    class A1State(State):
        a1v1 = definition(_greater_than(0))

    class B1(Story):
        I.b1s1
        I.a1
        I.b1s2

        b1s1 = m._assign_method("b1v1", 2)
        b1s2 = m._normal_method

        def __init__(self):
            self.a1 = A1()

    class B1State(State):
        a1v1 = definition(_less_than(2))
        b1v1 = definition(_greater_than(1))

    class C1(Story):
        I.c1s1
        I.b1
        I.c1s2

        c1s1 = m._assign_method("c1v1", 3)
        c1s2 = m._normal_method

        def __init__(self):
            self.b1 = B1()

    class C1State(State):
        a1v1 = definition(_equal_to(1))
        b1v1 = definition(_less_than(3))
        c1v1 = definition(_greater_than(2))

    # First level.

    story = A1()
    state_class = Union(C1State, B1State, A1State)
    state = state_class()
    r.run(story, state)
    assert state.a1v1 == 1

    # Second level.

    story = B1()
    state_class = Union(C1State, B1State, A1State)
    state = state_class()
    r.run(story, state)
    assert state.b1v1 == 2

    # Third level.

    story = C1()
    state_class = Union(C1State, B1State, A1State)
    state = state_class()
    r.run(story, state)
    assert state.c1v1 == 3


@pytest.mark.parametrize("definition", [Variable, Argument])
@pytest.mark.parametrize("unite", [Union, lambda *args: reduce(Union, args)])
@pytest.mark.parametrize("a1v1_value", [-1, 3])
@pytest.mark.parametrize("b1v1_value", [0, 4])
@pytest.mark.parametrize("c1v1_value", [1])
def test_state_union_merge_validators_failure(
    r, m, definition, unite, a1v1_value, b1v1_value, c1v1_value
):
    """Validator functions in state union should be merged."""

    class A1(Story):
        I.a1s1
        I.a1s2
        I.a1s3

        a1s1 = m._normal_method
        a1s2 = m._assign_method("a1v1", a1v1_value)
        a1s3 = m._normal_method

    class A1State(State):
        a1v1 = definition(_greater_than(0))

    class B1(Story):
        I.b1s1
        I.a1
        I.b1s2

        b1s1 = m._assign_method("b1v1", b1v1_value)
        b1s2 = m._normal_method

        def __init__(self):
            self.a1 = A1()

    class B1State(State):
        a1v1 = definition(_less_than(2))
        b1v1 = definition(_greater_than(1))

    class C1(Story):
        I.c1s1
        I.b1
        I.c1s2

        c1s1 = m._assign_method("c1v1", c1v1_value)
        c1s2 = m._normal_method

        def __init__(self):
            self.b1 = B1()

    class C1State(State):
        a1v1 = definition(_equal_to(1))
        b1v1 = definition(_less_than(3))
        c1v1 = definition(_greater_than(2))

    # First level.

    story = A1()
    state_class = unite(C1State, B1State, A1State)
    state = state_class()
    with pytest.raises(_ValidationError) as exc_info:
        r.run(story, state)
    assert not hasattr(state, "a1v1")
    assert exc_info.value.args == (a1v1_value,)

    # Second level.

    story = B1()
    state_class = unite(C1State, B1State, A1State)
    state = state_class()
    with pytest.raises(_ValidationError) as exc_info:
        r.run(story, state)
    assert not hasattr(state, "b1v1")
    assert exc_info.value.args == (b1v1_value,)

    # Third level.

    story = C1()
    state_class = unite(C1State, B1State, A1State)
    state = state_class()
    with pytest.raises(_ValidationError) as exc_info:
        r.run(story, state)
    assert not hasattr(state, "c1v1")
    assert exc_info.value.args == (c1v1_value,)
