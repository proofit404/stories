import pytest

import examples
from helpers import make_collector
from stories._context import Context
from stories._history import History
from stories.exceptions import FailureError


def test_context_dir():
    """Show context variables in the `dir` output."""

    class Ctx(object):
        a = 2
        b = 2

    assert dir(Context({"a": 2, "b": 2}, History("Obj", "meth"))) == dir(Ctx())


def test_context_representation():

    # TODO: Empty.

    expected = """
Empty.x()

Context()
    """.strip()

    # Collector, getter = make_collector(examples.methods.Empty, "two")
    # Collector().x()
    # assert repr(getter()) == expected
    #
    # Collector, getter = make_collector(examples.methods.Empty, "two")
    # Collector().x.run()
    # assert repr(getter()) == expected

    expected = """
EmptySubstory.y:
  x

Context()
        """.strip()

    # Collector, getter = make_collector(examples.methods.EmptySubstory, "x")
    # Collector().y()
    # assert repr(getter()) == expected
    #
    # Collector, getter = make_collector(examples.methods.EmptySubstory, "x")
    # Collector().y.run()
    # assert repr(getter()) == expected

    expected = """
SubstoryDI.y:
  x (Empty.x)

Context()
        """.strip()

    # Collector, getter = make_collector(examples.methods.SubstoryDI, "x")
    # Collector(examples.methods.Empty().x).y(3)
    # assert repr(getter()) == expected
    #
    # Collector, getter = make_collector(examples.methods.SubstoryDI, "x")
    # Collector(examples.methods.Empty().x).y.run(3)
    # assert repr(getter()) == expected

    # Failure.

    expected = """
Simple.x:
  one
  two (failed)

Context:
    foo = 2  # Story argument
    bar = 2  # Story argument
        """.strip()

    Collector, getter = make_collector(examples.methods.Simple, "two")
    with pytest.raises(FailureError):
        Collector().x(2, 2)
    assert repr(getter()) == expected

    Collector, getter = make_collector(examples.methods.Simple, "two")
    Collector().x.run(2, 2)
    assert repr(getter()) == expected

    expected = """
SimpleSubstory.y:
  start
  before
  x
    one
    two (failed)

Context:
    spam = 3  # Story argument
    foo = 2   # Set by SimpleSubstory.start
    bar = 4   # Set by SimpleSubstory.before
        """.strip()

    Collector, getter = make_collector(examples.methods.SimpleSubstory, "two")
    with pytest.raises(FailureError):
        Collector().y(3)
    assert repr(getter()) == expected

    Collector, getter = make_collector(examples.methods.SimpleSubstory, "two")
    Collector().y.run(3)
    assert repr(getter()) == expected

    expected = """
SubstoryDI.y:
  start
  before
  x (Simple.x)
    one
    two (failed)

Context:
    spam = 3  # Story argument
    foo = 2   # Set by SubstoryDI.start
    bar = 4   # Set by SubstoryDI.before
        """.strip()

    Collector, getter = make_collector(examples.methods.Simple, "two")
    with pytest.raises(FailureError):
        examples.methods.SubstoryDI(Collector().x).y(3)
    assert repr(getter()) == expected

    Collector, getter = make_collector(examples.methods.Simple, "two")
    examples.methods.SubstoryDI(Collector().x).y.run(3)
    assert repr(getter()) == expected

    # FIXME: Failure with reason.
    #
    #     expected = """
    # Simple.x:
    #   one
    #   two (failed: "'foo' is too big")
    #
    # Context:
    #     foo = 3  # Story argument
    #     bar = 2  # Story argument
    #         """.strip()
    #
    #     Collector, getter = make_collector(examples.methods.Simple, "two")
    #     with pytest.raises(FailureError):
    #         Collector().x(3, 2)
    #     assert repr(getter()) == expected
    #
    #     Collector, getter = make_collector(examples.methods.Simple, "two")
    #     Collector().x.run(3, 2)
    #     assert repr(getter()) == expected
    #
    #     expected = """
    # SimpleSubstory.y:
    #   start
    #   before
    #   x
    #     one
    #     two (failed: "'foo' is too big")
    #
    # Context:
    #     spam = 4  # Story argument
    #     foo = 3   # Set by SimpleSubstory.start
    #     bar = 5   # Set by SimpleSubstory.before
    #         """.strip()
    #
    #     Collector, getter = make_collector(examples.methods.SimpleSubstory, "two")
    #     with pytest.raises(FailureError):
    #         Collector().y(4)
    #     assert repr(getter()) == expected
    #
    #     Collector, getter = make_collector(examples.methods.SimpleSubstory, "two")
    #     Collector().y.run(4)
    #     assert repr(getter()) == expected
    #
    #     expected = """
    # SubstoryDI.y:
    #   start
    #   before
    #   x (Simple.x)
    #     one
    #     two (failed: "'foo' is too big")
    #
    # Context:
    #     spam = 4  # Story argument
    #     foo = 3   # Set by SubstoryDI.start
    #     bar = 5   # Set by SubstoryDI.before
    #         """.strip()
    #
    #     Collector, getter = make_collector(examples.methods.Simple, "two")
    #     with pytest.raises(FailureError):
    #         examples.methods.SubstoryDI(Collector().x).y(4)
    #     assert repr(getter()) == expected
    #
    #     Collector, getter = make_collector(examples.methods.Simple, "two")
    #     examples.methods.SubstoryDI(Collector().x).y.run(4)
    #     assert repr(getter()) == expected

    # Result.

    expected = """
Simple.x:
  one
  two
  three (returned: -1)

Context:
    foo = 1  # Story argument
    bar = 3  # Story argument
    baz = 4  # Set by Simple.two
        """.strip()

    Collector, getter = make_collector(examples.methods.Simple, "three")
    Collector().x(1, 3)
    assert repr(getter()) == expected

    Collector, getter = make_collector(examples.methods.Simple, "three")
    Collector().x.run(1, 3)
    assert repr(getter()) == expected

    expected = """
SimpleSubstory.y:
  start
  before
  x
    one
    two
    three (returned: -1)

Context:
    spam = 2  # Story argument
    foo = 1   # Set by SimpleSubstory.start
    bar = 3   # Set by SimpleSubstory.before
    baz = 4   # Set by SimpleSubstory.two
        """.strip()

    Collector, getter = make_collector(examples.methods.SimpleSubstory, "three")
    Collector().y(2)
    assert repr(getter()) == expected

    Collector, getter = make_collector(examples.methods.SimpleSubstory, "three")
    Collector().y.run(2)
    assert repr(getter()) == expected

    expected = """
SubstoryDI.y:
  start
  before
  x (Simple.x)
    one
    two
    three (returned: -1)

Context:
    spam = 2  # Story argument
    foo = 1   # Set by SubstoryDI.start
    bar = 3   # Set by SubstoryDI.before
    baz = 4   # Set by Simple.two
    """.strip()

    Collector, getter = make_collector(examples.methods.Simple, "three")
    examples.methods.SubstoryDI(Collector().x).y(2)
    assert repr(getter()) == expected

    Collector, getter = make_collector(examples.methods.Simple, "three")
    examples.methods.SubstoryDI(Collector().x).y.run(2)
    assert repr(getter()) == expected

    expected = """
SubstoryDI.y:
  start
  before
  x (Pipe.x)
    one
    two
    three
  after (returned: 6)

Context:
    spam = 3  # Story argument
    foo = 2   # Set by SubstoryDI.start
    bar = 4   # Set by SubstoryDI.before
        """.strip()

    Collector, getter = make_collector(examples.methods.SubstoryDI, "after")
    Collector(examples.methods.Pipe().x).y(3)
    assert repr(getter()) == expected

    Collector, getter = make_collector(examples.methods.SubstoryDI, "after")
    Collector(examples.methods.Pipe().x).y.run(3)
    assert repr(getter()) == expected

    # Skip.

    expected = """
Simple.x:
  one
  two (skipped)

Context:
    foo = 1   # Story argument
    bar = -1  # Story argument
        """.strip()

    Collector, getter = make_collector(examples.methods.Simple, "two")
    Collector().x(1, -1)
    assert repr(getter()) == expected

    Collector, getter = make_collector(examples.methods.Simple, "two")
    Collector().x.run(1, -1)
    assert repr(getter()) == expected

    expected = """
SimpleSubstory.y:
  start
  before
  x
    one
    two (skipped)
  after (returned: -4)

Context:
    spam = -2  # Story argument
    foo = -3   # Set by SimpleSubstory.start
    bar = -1   # Set by SimpleSubstory.before
        """.strip()

    Collector, getter = make_collector(examples.methods.SimpleSubstory, "after")
    Collector().y(-2)
    assert repr(getter()) == expected

    Collector, getter = make_collector(examples.methods.SimpleSubstory, "after")
    Collector().y.run(-2)
    assert repr(getter()) == expected

    expected = """
SubstoryDI.y:
  start
  before
  x (Simple.x)
    one
    two (skipped)
  after (returned: -4)

Context:
    spam = -2  # Story argument
    foo = -3   # Set by SubstoryDI.start
    bar = -1   # Set by SubstoryDI.before
        """.strip()

    Collector, getter = make_collector(examples.methods.SubstoryDI, "after")
    Collector(examples.methods.Simple().x).y(-2)
    assert repr(getter()) == expected

    Collector, getter = make_collector(examples.methods.SubstoryDI, "after")
    Collector(examples.methods.Simple().x).y.run(-2)
    assert repr(getter()) == expected

    expected = """
SubstoryDI.y:
  start
  before
  x (SimpleSubstory.z)
    first (skipped)
  after (returned: 4)

Context:
    spam = 2  # Story argument
    foo = 1   # Set by SubstoryDI.start
    bar = 3   # Set by SubstoryDI.before
        """.strip()

    Collector, getter = make_collector(examples.methods.SubstoryDI, "after")
    Collector(examples.methods.SimpleSubstory().z).y(2)
    assert repr(getter()) == expected

    Collector, getter = make_collector(examples.methods.SubstoryDI, "after")
    Collector(examples.methods.SimpleSubstory().z).y.run(2)
    assert repr(getter()) == expected

    # Error.

    expected = """
StepError.x:
  one (errored: Exception)

Context()
    """.strip()

    Collector, getter = make_collector(examples.methods.StepError, "one")
    with pytest.raises(Exception):
        Collector().x()
    assert repr(getter()) == expected

    Collector, getter = make_collector(examples.methods.StepError, "one")
    with pytest.raises(Exception):
        Collector().x.run()
    assert repr(getter()) == expected
