from types import SimpleNamespace

import pytest

from fixtures import S
from stories import I


def test_return_value(s: S) -> None:
    class A1(s.Story):
        I.a1s1
        I.a1s2
        I.a1s3

        a1s1 = s.normal_method
        a1s2 = s.normal_method
        a1s3 = s.normal_method

    class B1(s.Story):
        I.b1s1
        I.a1
        I.b1s2

        b1s1 = s.normal_method
        b1s2 = s.normal_method

        def __init__(self) -> None:
            self.a1 = A1()

    class C1(s.Story):
        I.c1s1
        I.b1
        I.c1s2

        c1s1 = s.normal_method
        c1s2 = s.normal_method

        def __init__(self) -> None:
            self.b1 = B1()

    # First level.

    story = A1()
    state = SimpleNamespace()
    assert s.run(story, state) is None

    # Second level.

    story = B1()
    state = SimpleNamespace()
    assert s.run(story, state) is None

    # Third level.

    story = C1()
    state = SimpleNamespace()
    assert s.run(story, state) is None


def test_execute_steps(s: S) -> None:
    class A1(s.Story):
        I.a1s1
        I.a1s2
        I.a1s3

        a1s1 = s.append_method("calls", "a1s1")
        a1s2 = s.append_method("calls", "a1s2")
        a1s3 = s.append_method("calls", "a1s3")

    class B1(s.Story):
        I.b1s1
        I.a1
        I.b1s2

        b1s1 = s.append_method("calls", "b1s1")
        b1s2 = s.append_method("calls", "b1s2")

        def __init__(self) -> None:
            self.a1 = A1()

    class C1(s.Story):
        I.c1s1
        I.b1
        I.c1s2

        c1s1 = s.append_method("calls", "c1s1")
        c1s2 = s.append_method("calls", "c1s2")

        def __init__(self) -> None:
            self.b1 = B1()

    # First level.

    story = A1()
    state = SimpleNamespace(calls=[])
    s.run(story, state)
    assert state.calls == ["a1s1", "a1s2", "a1s3"]

    # Second level.

    story = B1()
    state = SimpleNamespace(calls=[])
    s.run(story, state)
    assert state.calls == ["b1s1", "a1s1", "a1s2", "a1s3", "b1s2"]

    # Third level.

    story = C1()
    state = SimpleNamespace(calls=[])
    s.run(story, state)
    assert state.calls == ["c1s1", "b1s1", "a1s1", "a1s2", "a1s3", "b1s2", "c1s2"]


def test_assign_state_attribute(s: S) -> None:
    class A1(s.Story):
        I.a1s1
        I.a1s2

        a1s1 = s.assign_method("a1v1", 1)
        a1s2 = s.assert_method("a1v1", 1)

    class B1(s.Story):
        I.b1s1
        I.a1
        I.b1s2

        b1s1 = s.assign_method("b1v1", 2)
        b1s2 = s.assert_method("b1v1", 2)

        def __init__(self) -> None:
            self.a1 = A1()

    class C1(s.Story):
        I.c1s1
        I.b1
        I.c1s2

        c1s1 = s.assign_method("c1v1", 3)
        c1s2 = s.assert_method("c1v1", 3)

        def __init__(self) -> None:
            self.b1 = B1()

    # First level.

    story = A1()
    state = SimpleNamespace()
    s.run(story, state)

    # Second level.

    story = B1()
    state = SimpleNamespace()
    s.run(story, state)

    # Third level.

    story = C1()
    state = SimpleNamespace()
    s.run(story, state)


def test_access_state_attributes(s: S) -> None:
    class A1(s.Story):
        I.a1s1
        I.a1s2
        I.a1s3

        a1s1 = s.normal_method
        a1s2 = s.assign_method("a1v1", 1)
        a1s3 = s.normal_method

    class B1(s.Story):
        I.b1s1
        I.a1
        I.b1s2

        b1s1 = s.assign_method("b1v1", 2)
        b1s2 = s.normal_method

        def __init__(self) -> None:
            self.a1 = A1()

    class C1(s.Story):
        I.c1s1
        I.b1
        I.c1s2

        c1s1 = s.assign_method("c1v1", 3)
        c1s2 = s.normal_method

        def __init__(self) -> None:
            self.b1 = B1()

    # First level.

    story = A1()
    state = SimpleNamespace()
    s.run(story, state)
    assert state.a1v1 == 1

    # Second level.

    story = B1()
    state = SimpleNamespace()
    s.run(story, state)
    assert state.a1v1 == 1
    assert state.b1v1 == 2

    # Third level.

    story = C1()
    state = SimpleNamespace()
    s.run(story, state)
    assert state.a1v1 == 1
    assert state.b1v1 == 2
    assert state.c1v1 == 3


def test_propagate_exceptions(s: S) -> None:
    class A1(s.Story):
        I.a1s1
        I.a1s2
        I.a1s3

        a1s1 = s.normal_method
        a1s2 = s.normal_method
        a1s3 = s.error_method("error in a1s3")

    class B1(s.Story):
        I.b1s1
        I.a1
        I.b1s2

        b1s1 = s.error_method("error in b1s1")
        b1s2 = s.normal_method

        def __init__(self) -> None:
            self.a1 = A1()

    class C1(s.Story):
        I.c1s1
        I.b1
        I.c1s2

        c1s1 = s.error_method("error in c1s1")
        c1s2 = s.normal_method

        def __init__(self) -> None:
            self.b1 = B1()

    # First level.

    story = A1()
    state = SimpleNamespace()
    with pytest.raises(s.StepError) as exc_info:
        s.run(story, state)
    assert isinstance(exc_info.value, s.StepError)
    assert str(exc_info.value) == "error in a1s3"

    # Second level.

    story = B1()
    state = SimpleNamespace()
    with pytest.raises(s.StepError) as exc_info:
        s.run(story, state)
    assert isinstance(exc_info.value, s.StepError)
    assert str(exc_info.value) == "error in b1s1"

    # Third level.

    story = C1()
    state = SimpleNamespace()
    with pytest.raises(s.StepError) as exc_info:
        s.run(story, state)
    assert isinstance(exc_info.value, s.StepError)
    assert str(exc_info.value) == "error in c1s1"
