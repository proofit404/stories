"""Tests related to stories module."""
import pytest

from stories import I
from stories import State
from stories import Story


def test_return_value(r, m):
    """Story should not return any value."""

    class A1(Story):
        I.a1s1
        I.a1s2
        I.a1s3

        a1s1 = m._normal_method
        a1s2 = m._normal_method
        a1s3 = m._normal_method

    class B1(Story):
        I.b1s1
        I.a1
        I.b1s2

        b1s1 = m._normal_method
        b1s2 = m._normal_method

        def __init__(self):
            self.a1 = A1()

    class C1(Story):
        I.c1s1
        I.b1
        I.c1s2

        c1s1 = m._normal_method
        c1s2 = m._normal_method

        def __init__(self):
            self.b1 = B1()

    # First level.

    story = A1()
    state = State()
    assert r.run(story, state) is None

    # Second level.

    story = B1()
    state = State()
    assert r.run(story, state) is None

    # Third level.

    story = C1()
    state = State()
    assert r.run(story, state) is None


def test_execute_steps(r, m):
    """Story steps should be executed according to the given order."""

    class A1(Story):
        I.a1s1
        I.a1s2
        I.a1s3

        a1s1 = m._append_method("calls", "a1s1")
        a1s2 = m._append_method("calls", "a1s2")
        a1s3 = m._append_method("calls", "a1s3")

    class B1(Story):
        I.b1s1
        I.a1
        I.b1s2

        b1s1 = m._append_method("calls", "b1s1")
        b1s2 = m._append_method("calls", "b1s2")

        def __init__(self):
            self.a1 = A1()

    class C1(Story):
        I.c1s1
        I.b1
        I.c1s2

        c1s1 = m._append_method("calls", "c1s1")
        c1s2 = m._append_method("calls", "c1s2")

        def __init__(self):
            self.b1 = B1()

    # First level.

    story = A1()
    state = State(calls=[])
    r.run(story, state)
    assert state.calls == ["a1s1", "a1s2", "a1s3"]

    # Second level.

    story = B1()
    state = State(calls=[])
    r.run(story, state)
    assert state.calls == ["b1s1", "a1s1", "a1s2", "a1s3", "b1s2"]

    # Third level.

    story = C1()
    state = State(calls=[])
    r.run(story, state)
    assert state.calls == ["c1s1", "b1s1", "a1s1", "a1s2", "a1s3", "b1s2", "c1s2"]


def test_propagate_exceptions(r, m):
    """Exceptions raised by story steps should be propagated to the caller."""

    class A1(Story):
        I.a1s1
        I.a1s2
        I.a1s3

        a1s1 = m._normal_method
        a1s2 = m._normal_method
        a1s3 = m._error_method("error in a1s3")

    class B1(Story):
        I.b1s1
        I.a1
        I.b1s2

        b1s1 = m._error_method("error in b1s1")
        b1s2 = m._normal_method

        def __init__(self):
            self.a1 = A1()

    class C1(Story):
        I.c1s1
        I.b1
        I.c1s2

        c1s1 = m._error_method("error in c1s1")
        c1s2 = m._normal_method

        def __init__(self):
            self.b1 = B1()

    # First level.

    story = A1()
    state = State()
    with pytest.raises(m._StepError) as exc_info:
        r.run(story, state)
    assert isinstance(exc_info.value, m._StepError)
    assert str(exc_info.value) == "error in a1s3"

    # Second level.

    story = B1()
    state = State()
    with pytest.raises(m._StepError) as exc_info:
        r.run(story, state)
    assert isinstance(exc_info.value, m._StepError)
    assert str(exc_info.value) == "error in b1s1"

    # Third level.

    story = C1()
    state = State()
    with pytest.raises(m._StepError) as exc_info:
        r.run(story, state)
    assert isinstance(exc_info.value, m._StepError)
    assert str(exc_info.value) == "error in c1s1"
