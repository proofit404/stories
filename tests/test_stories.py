from types import SimpleNamespace
from typing import Any

import pytest

from stories import I


def test_return_value(s: Any) -> None:
    class A1(s.Story):  # type: ignore[misc,no-any-unimported]
        I.a1s1
        I.a1s2
        I.a1s3

        a1s1 = s.normal_method
        a1s2 = s.normal_method
        a1s3 = s.normal_method

    class B1(s.Story):  # type: ignore[misc,no-any-unimported]
        I.b1s1
        I.a1
        I.b1s2

        b1s1 = s.normal_method
        b1s2 = s.normal_method

        def __init__(self) -> None:
            self.a1 = A1()

    class C1(s.Story):  # type: ignore[misc,no-any-unimported]
        I.c1s1
        I.b1
        I.c1s2

        c1s1 = s.normal_method
        c1s2 = s.normal_method

        def __init__(self) -> None:
            self.b1 = B1()

    # First level.

    story_a = A1()
    state_a = SimpleNamespace()
    assert s.run(story_a, state_a) is None

    # Second level.

    story_b = B1()
    state_b = SimpleNamespace()
    assert s.run(story_b, state_b) is None

    # Third level.

    story_c = C1()
    state_c = SimpleNamespace()
    assert s.run(story_c, state_c) is None


def test_execute_steps(s: Any) -> None:
    class A1(s.Story):  # type: ignore[misc,no-any-unimported]
        I.a1s1
        I.a1s2
        I.a1s3

        a1s1 = s.append_method("calls", "a1s1")
        a1s2 = s.append_method("calls", "a1s2")
        a1s3 = s.append_method("calls", "a1s3")

    class B1(s.Story):  # type: ignore[misc,no-any-unimported]
        I.b1s1
        I.a1
        I.b1s2

        b1s1 = s.append_method("calls", "b1s1")
        b1s2 = s.append_method("calls", "b1s2")

        def __init__(self) -> None:
            self.a1 = A1()

    class C1(s.Story):  # type: ignore[misc,no-any-unimported]
        I.c1s1
        I.b1
        I.c1s2

        c1s1 = s.append_method("calls", "c1s1")
        c1s2 = s.append_method("calls", "c1s2")

        def __init__(self) -> None:
            self.b1 = B1()

    # First level.

    story_a = A1()
    state_a = SimpleNamespace(calls=[])
    s.run(story_a, state_a)
    assert state_a.calls == ["a1s1", "a1s2", "a1s3"]

    # Second level.

    story_b = B1()
    state_b = SimpleNamespace(calls=[])
    s.run(story_b, state_b)
    assert state_b.calls == ["b1s1", "a1s1", "a1s2", "a1s3", "b1s2"]

    # Third level.

    story_c = C1()
    state_c = SimpleNamespace(calls=[])
    s.run(story_c, state_c)
    assert state_c.calls == ["c1s1", "b1s1", "a1s1", "a1s2", "a1s3", "b1s2", "c1s2"]


def test_assign_state_attribute(s: Any) -> None:
    class A1(s.Story):  # type: ignore[misc,no-any-unimported]
        I.a1s1
        I.a1s2

        a1s1 = s.assign_method("a1v1", 1)
        a1s2 = s.assert_method("a1v1", 1)

    class B1(s.Story):  # type: ignore[misc,no-any-unimported]
        I.b1s1
        I.a1
        I.b1s2

        b1s1 = s.assign_method("b1v1", 2)
        b1s2 = s.assert_method("b1v1", 2)

        def __init__(self) -> None:
            self.a1 = A1()

    class C1(s.Story):  # type: ignore[misc,no-any-unimported]
        I.c1s1
        I.b1
        I.c1s2

        c1s1 = s.assign_method("c1v1", 3)
        c1s2 = s.assert_method("c1v1", 3)

        def __init__(self) -> None:
            self.b1 = B1()

    # First level.

    story_a = A1()
    state_a = SimpleNamespace()
    s.run(story_a, state_a)

    # Second level.

    story_b = B1()
    state_b = SimpleNamespace()
    s.run(story_b, state_b)

    # Third level.

    story_c = C1()
    state_c = SimpleNamespace()
    s.run(story_c, state_c)


def test_access_state_attributes(s: Any) -> None:
    class A1(s.Story):  # type: ignore[misc,no-any-unimported]
        I.a1s1
        I.a1s2
        I.a1s3

        a1s1 = s.normal_method
        a1s2 = s.assign_method("a1v1", 1)
        a1s3 = s.normal_method

    class B1(s.Story):  # type: ignore[misc,no-any-unimported]
        I.b1s1
        I.a1
        I.b1s2

        b1s1 = s.assign_method("b1v1", 2)
        b1s2 = s.normal_method

        def __init__(self) -> None:
            self.a1 = A1()

    class C1(s.Story):  # type: ignore[misc,no-any-unimported]
        I.c1s1
        I.b1
        I.c1s2

        c1s1 = s.assign_method("c1v1", 3)
        c1s2 = s.normal_method

        def __init__(self) -> None:
            self.b1 = B1()

    # First level.

    story_a = A1()
    state_a = SimpleNamespace()
    s.run(story_a, state_a)
    assert state_a.a1v1 == 1

    # Second level.

    story_b = B1()
    state_b = SimpleNamespace()
    s.run(story_b, state_b)
    assert state_b.a1v1 == 1
    assert state_b.b1v1 == 2

    # Third level.

    story_c = C1()
    state_c = SimpleNamespace()
    s.run(story_c, state_c)
    assert state_c.a1v1 == 1
    assert state_c.b1v1 == 2
    assert state_c.c1v1 == 3


def test_propagate_exceptions(s: Any) -> None:
    class A1(s.Story):  # type: ignore[misc,no-any-unimported]
        I.a1s1
        I.a1s2
        I.a1s3

        a1s1 = s.normal_method
        a1s2 = s.normal_method
        a1s3 = s.error_method("error in a1s3")

    class B1(s.Story):  # type: ignore[misc,no-any-unimported]
        I.b1s1
        I.a1
        I.b1s2

        b1s1 = s.error_method("error in b1s1")
        b1s2 = s.normal_method

        def __init__(self) -> None:
            self.a1 = A1()

    class C1(s.Story):  # type: ignore[misc,no-any-unimported]
        I.c1s1
        I.b1
        I.c1s2

        c1s1 = s.error_method("error in c1s1")
        c1s2 = s.normal_method

        def __init__(self) -> None:
            self.b1 = B1()

    # First level.

    story_a = A1()
    state_a = SimpleNamespace()
    with pytest.raises(s.StepError) as exc_info:
        s.run(story_a, state_a)
    assert isinstance(exc_info.value, s.StepError)
    assert str(exc_info.value) == "error in a1s3"

    # Second level.

    story_b = B1()
    state_b = SimpleNamespace()
    with pytest.raises(s.StepError) as exc_info:
        s.run(story_b, state_b)
    assert isinstance(exc_info.value, s.StepError)
    assert str(exc_info.value) == "error in b1s1"

    # Third level.

    story_c = C1()
    state_c = SimpleNamespace()
    with pytest.raises(s.StepError) as exc_info:
        s.run(story_c, state_c)
    assert isinstance(exc_info.value, s.StepError)
    assert str(exc_info.value) == "error in c1s1"
