import examples
import pytest
from helpers import make_collector
from stories import Failure, Result, Skip, Success
from stories._context import Context
from stories.exceptions import FailureError


def test_empty():

    result = examples.Empty().x()
    assert result is None

    result = examples.Empty().x.run()
    assert result.is_success
    assert not result.is_failure
    assert result.value is None

    result = examples.EmptySubstory().y()
    assert result is None

    result = examples.EmptySubstory().y.run()
    assert result.is_success
    assert not result.is_failure
    assert result.value is None

    result = examples.SubstoryDI(examples.Empty().x).y(3)
    assert result == 6

    result = examples.SubstoryDI(examples.Empty().x).y.run(3)
    assert result.is_success
    assert not result.is_failure
    assert result.value == 6


def test_failure():

    # Simple.

    with pytest.raises(FailureError) as exc_info:
        examples.Simple().x(2, 2)
    assert not exc_info.value.reason

    result = examples.Simple().x.run(2, 2)
    assert not result.is_success
    assert result.is_failure
    assert not result.reason
    assert result.ctx == {"foo": 2, "bar": 2}
    assert result.failed_on("two")
    assert not result.failed_on("one")
    assert result.failed_because(None)
    assert not result.failed_because("'foo' is too big")
    with pytest.raises(AssertionError):
        result.value

    # Simple with reason.

    with pytest.raises(FailureError) as exc_info:
        examples.Simple().x(3, 2)
    assert exc_info.value.reason == "'foo' is too big"

    result = examples.Simple().x.run(3, 2)
    assert not result.is_success
    assert result.is_failure
    assert result.reason == "'foo' is too big"
    assert result.ctx == {"foo": 3, "bar": 2}
    assert result.failed_on("two")
    assert not result.failed_on("one")
    assert result.failed_because("'foo' is too big")
    assert not result.failed_because(None)
    with pytest.raises(AssertionError):
        result.value

    # Simple substory.

    with pytest.raises(FailureError) as exc_info:
        examples.SimpleSubstory().y(3)
    assert not exc_info.value.reason

    result = examples.SimpleSubstory().y.run(3)
    assert not result.is_success
    assert result.is_failure
    assert not result.reason
    assert result.ctx == {"foo": 2, "bar": 4, "spam": 3}
    assert result.failed_on("two")
    assert not result.failed_on("one")
    assert result.failed_because(None)
    assert not result.failed_because("'foo' is too big")
    with pytest.raises(AssertionError):
        result.value

    # Simple substory with reason.

    with pytest.raises(FailureError) as exc_info:
        examples.SimpleSubstory().y(4)
    assert exc_info.value.reason == "'foo' is too big"

    result = examples.SimpleSubstory().y.run(4)
    assert not result.is_success
    assert result.is_failure
    assert result.reason == "'foo' is too big"
    assert result.ctx == {"foo": 3, "bar": 5, "spam": 4}
    assert result.failed_on("two")
    assert not result.failed_on("one")
    assert result.failed_because("'foo' is too big")
    assert not result.failed_because(None)
    with pytest.raises(AssertionError):
        result.value

    # Substory DI.

    with pytest.raises(FailureError) as exc_info:
        examples.SubstoryDI(examples.Simple().x).y(3)
    assert not exc_info.value.reason

    result = examples.SubstoryDI(examples.Simple().x).y.run(3)
    assert not result.is_success
    assert result.is_failure
    assert not result.reason
    assert result.ctx == {"foo": 2, "bar": 4, "spam": 3}
    assert result.failed_on("two")
    assert not result.failed_on("one")
    assert result.failed_because(None)
    assert not result.failed_because("'foo' is too big")
    with pytest.raises(AssertionError):
        result.value

    # Substory DI with reason.

    with pytest.raises(FailureError) as exc_info:
        examples.SubstoryDI(examples.Simple().x).y(4)
    assert exc_info.value.reason == "'foo' is too big"

    result = examples.SubstoryDI(examples.Simple().x).y.run(4)
    assert not result.is_success
    assert result.is_failure
    assert result.reason == "'foo' is too big"
    assert result.ctx == {"foo": 3, "bar": 5, "spam": 4}
    assert result.failed_on("two")
    assert not result.failed_on("one")
    assert result.failed_because("'foo' is too big")
    assert not result.failed_because(None)
    with pytest.raises(AssertionError):
        result.value


def test_result():

    result = examples.Simple().x(1, 3)
    assert result == -1

    result = examples.Simple().x.run(1, 3)
    assert result.is_success
    assert not result.is_failure
    assert not result.failed_on("two")
    assert not result.failed_because("'foo' is too big")
    assert result.value == -1

    result = examples.SimpleSubstory().y(2)
    assert result == -1

    result = examples.SimpleSubstory().y.run(2)
    assert result.is_success
    assert not result.is_failure
    assert not result.failed_on("two")
    assert not result.failed_because("'foo' is too big")
    assert result.value == -1

    result = examples.SubstoryDI(examples.Simple().x).y(2)
    assert result == -1

    result = examples.SubstoryDI(examples.Simple().x).y.run(2)
    assert result.is_success
    assert not result.is_failure
    assert not result.failed_on("two")
    assert not result.failed_because("'foo' is too big")
    assert result.value == -1


def test_skip():

    result = examples.Simple().x(1, -1)
    assert result is None

    result = examples.Simple().x.run(1, -1)
    assert result.is_success
    assert not result.is_failure
    assert result.value is None

    result = examples.SimpleSubstory().y(-2)
    assert result == -4

    result = examples.SimpleSubstory().y.run(-2)
    assert result.is_success
    assert not result.is_failure
    assert result.value == -4

    result = examples.SubstoryDI(examples.Simple().x).y(-2)
    assert result == -4

    result = examples.SubstoryDI(examples.Simple().x).y.run(-2)
    assert result.is_success
    assert not result.is_failure
    assert result.value == -4

    result = examples.SubstoryDI(examples.SimpleSubstory().z).y(2)
    assert result == 4

    result = examples.SubstoryDI(examples.SimpleSubstory().z).y.run(2)
    assert result.is_success
    assert not result.is_failure
    assert result.value == 4


def test_arguments_validation():

    with pytest.raises(AssertionError):
        examples.Simple().x(1)

    with pytest.raises(AssertionError):
        examples.Simple().x.run(1)

    with pytest.raises(AssertionError):
        examples.Simple().x(1, b=2)

    with pytest.raises(AssertionError):
        examples.Simple().x.run(1, b=2)


def test_context_immutability():

    with pytest.raises(AssertionError):
        examples.ExistedKey().x(a=1)

    with pytest.raises(AssertionError):
        examples.ExistedKey().x.run(a=1)


def test_return_type():

    with pytest.raises(AssertionError):
        examples.WrongResult().x()

    with pytest.raises(AssertionError):
        examples.WrongResult().x.run()


def test_attribute_access():

    result = examples.AttributeAccess().x()
    assert result is True

    result = examples.AttributeAccess().x.run()
    assert result.is_success
    assert not result.is_failure
    assert result.value is True


def test_inject_implementation():

    result = examples.ImplementationDI(f=lambda arg: arg + 1).x(1)
    assert result == 2

    result = examples.ImplementationDI(f=lambda arg: arg + 1).x.run(1)
    assert result.is_success
    assert not result.is_failure
    assert result.value == 2


def test_story_representation():

    story = repr(examples.Empty().x)
    expected = (
        """
Empty.x
  <empty>
""".strip()
    )
    assert story == expected

    story = repr(examples.EmptySubstory().y)
    expected = (
        """
EmptySubstory.y
  x
    <empty>
""".strip()
    )
    assert story == expected

    story = repr(examples.SubstoryDI(examples.Empty().x).y)
    expected = (
        """
SubstoryDI.y
  before
  x (Empty.x)
    <empty>
  after
""".strip()
    )
    assert story == expected

    story = repr(examples.Simple().x)
    expected = (
        """
Simple.x
  one
  two
  three
""".strip()
    )
    assert story == expected

    story = repr(examples.SimpleSubstory().y)
    expected = (
        """
SimpleSubstory.y
  before
  x
    one
    two
    three
  after
""".strip()
    )
    assert story == expected

    story = repr(examples.SubstoryDI(examples.Simple().x).y)
    expected = (
        """
SubstoryDI.y
  before
  x (Simple.x)
    one
    two
    three
  after
""".strip()
    )
    assert story == expected

    story = repr(examples.SubstoryDI(examples.SimpleSubstory().z).y)
    expected = (
        """
SubstoryDI.y
  before
  x (SimpleSubstory.z)
    first
    x
      one
      two
      three
  after
""".strip()
    )
    assert story == expected


def test_result_representation():

    result = Result(1)
    assert repr(result) == "Result(1)"


def test_success_representation():

    success = Success(foo="bar", baz=2)
    assert repr(success) in {"Success(foo='bar', baz=2)", "Success(baz=2, foo='bar')"}


def test_failure_representation():

    failure = Failure()
    assert repr(failure) == "Failure()"


def test_skip_representation():

    skip = Skip()
    assert repr(skip) == "Skip()"


def test_context_representation():

    assert repr(Context({})) == "Context()"

    expected = (
        """
Context:
    foo = 1  # Story argument
    bar = 3  # Story argument
    baz = 4  # Set by Simple.two
        """.strip()
    )

    Collector, getter = make_collector(examples.Simple, "three")
    Collector().x(1, 3)
    assert repr(getter().ctx) == expected

    Collector, getter = make_collector(examples.Simple, "three")
    Collector().x.run(1, 3)
    assert repr(getter().ctx) == expected

    expected = (
        """
Context:
    spam = 2  # Story argument
    foo = 1   # Set by SimpleSubstory.before
    bar = 3   # Set by SimpleSubstory.before
    baz = 4   # Set by SimpleSubstory.two
    """.strip()
    )

    Collector, getter = make_collector(examples.SimpleSubstory, "three")
    Collector().y(2)
    assert repr(getter().ctx) == expected

    Collector, getter = make_collector(examples.SimpleSubstory, "three")
    Collector().y.run(2)
    assert repr(getter().ctx) == expected

    expected = (
        """
Context:
    spam = 2  # Story argument
    foo = 1   # Set by SubstoryDI.before
    bar = 3   # Set by SubstoryDI.before
    baz = 4   # Set by Simple.two
    """.strip()
    )

    Collector, getter = make_collector(examples.Simple, "three")
    examples.SubstoryDI(Collector().x).y(2)
    assert repr(getter().ctx) == expected

    Collector, getter = make_collector(examples.Simple, "three")
    examples.SubstoryDI(Collector().x).y.run(2)
    assert repr(getter().ctx) == expected


def test_context_dir():
    """Show context variables in the `dir` output."""

    class Ctx(object):
        a = 2
        b = 2

    assert dir(Context({"a": 2, "b": 2})) == dir(Ctx())


def test_proxy_representation():

    # TODO: Empty.

    expected = "Proxy(Empty.x)"

    # Collector, getter = make_collector(examples.Empty, "two")
    # Collector().x()
    # assert repr(getter()) == expected
    #
    # Collector, getter = make_collector(examples.Empty, "two")
    # Collector().x.run()
    # assert repr(getter()) == expected

    expected = (
        """
Proxy(EmptySubstory.y):
  x
        """.strip()
    )

    # Collector, getter = make_collector(examples.EmptySubstory, "x")
    # Collector().y()
    # assert repr(getter()) == expected
    #
    # Collector, getter = make_collector(examples.EmptySubstory, "x")
    # Collector().y.run()
    # assert repr(getter()) == expected

    expected = (
        """
Proxy(SubstoryDI.y):
  x (Empty.x)
        """.strip()
    )

    # Collector, getter = make_collector(examples.SubstoryDI, "x")
    # Collector(examples.Empty().x).y(3)
    # assert repr(getter()) == expected
    #
    # Collector, getter = make_collector(examples.SubstoryDI, "x")
    # Collector(examples.Empty().x).y.run(3)
    # assert repr(getter()) == expected

    # Failure.

    expected = (
        """
Proxy(Simple.x):
  one
  two (failed)
        """.strip()
    )

    Collector, getter = make_collector(examples.Simple, "two")
    with pytest.raises(FailureError):
        Collector().x(2, 2)
    assert repr(getter()) == expected

    Collector, getter = make_collector(examples.Simple, "two")
    Collector().x.run(2, 2)
    assert repr(getter()) == expected

    expected = (
        """
Proxy(SimpleSubstory.y):
  before
  x
    one
    two (failed)
        """.strip()
    )

    Collector, getter = make_collector(examples.SimpleSubstory, "two")
    with pytest.raises(FailureError):
        Collector().y(3)
    assert repr(getter()) == expected

    Collector, getter = make_collector(examples.SimpleSubstory, "two")
    Collector().y.run(3)
    assert repr(getter()) == expected

    expected = (
        """
Proxy(SubstoryDI.y):
  before
  x (Simple.x)
    one
    two (failed)
        """.strip()
    )

    Collector, getter = make_collector(examples.Simple, "two")
    with pytest.raises(FailureError):
        examples.SubstoryDI(Collector().x).y(3)
    assert repr(getter()) == expected

    Collector, getter = make_collector(examples.Simple, "two")
    examples.SubstoryDI(Collector().x).y.run(3)
    assert repr(getter()) == expected

    # Failure with reason.

    expected = (
        """
Proxy(Simple.x):
  one
  two (failed: "'foo' is too big")
        """.strip()
    )

    Collector, getter = make_collector(examples.Simple, "two")
    with pytest.raises(FailureError):
        Collector().x(3, 2)
    assert repr(getter()) == expected

    Collector, getter = make_collector(examples.Simple, "two")
    Collector().x.run(3, 2)
    assert repr(getter()) == expected

    expected = (
        """
Proxy(SimpleSubstory.y):
  before
  x
    one
    two (failed: "'foo' is too big")
        """.strip()
    )

    Collector, getter = make_collector(examples.SimpleSubstory, "two")
    with pytest.raises(FailureError):
        Collector().y(4)
    assert repr(getter()) == expected

    Collector, getter = make_collector(examples.SimpleSubstory, "two")
    Collector().y.run(4)
    assert repr(getter()) == expected

    expected = (
        """
Proxy(SubstoryDI.y):
  before
  x (Simple.x)
    one
    two (failed: "'foo' is too big")
        """.strip()
    )

    Collector, getter = make_collector(examples.Simple, "two")
    with pytest.raises(FailureError):
        examples.SubstoryDI(Collector().x).y(4)
    assert repr(getter()) == expected

    Collector, getter = make_collector(examples.Simple, "two")
    examples.SubstoryDI(Collector().x).y.run(4)
    assert repr(getter()) == expected

    # Result.

    expected = (
        """
Proxy(Simple.x):
  one
  two
  three (returned: -1)
        """.strip()
    )

    Collector, getter = make_collector(examples.Simple, "three")
    Collector().x(1, 3)
    assert repr(getter()) == expected

    Collector, getter = make_collector(examples.Simple, "three")
    Collector().x.run(1, 3)
    assert repr(getter()) == expected

    expected = (
        """
Proxy(SimpleSubstory.y):
  before
  x
    one
    two
    three (returned: -1)
        """.strip()
    )

    Collector, getter = make_collector(examples.SimpleSubstory, "three")
    Collector().y(2)
    assert repr(getter()) == expected

    Collector, getter = make_collector(examples.SimpleSubstory, "three")
    Collector().y.run(2)
    assert repr(getter()) == expected

    expected = (
        """
Proxy(SubstoryDI.y):
  before
  x (Simple.x)
    one
    two
    three (returned: -1)
    """.strip()
    )

    Collector, getter = make_collector(examples.Simple, "three")
    examples.SubstoryDI(Collector().x).y(2)
    assert repr(getter()) == expected

    Collector, getter = make_collector(examples.Simple, "three")
    examples.SubstoryDI(Collector().x).y.run(2)
    assert repr(getter()) == expected

    # Skip.

    expected = (
        """
Proxy(Simple.x):
  one
  two (skipped)
        """.strip()
    )

    Collector, getter = make_collector(examples.Simple, "two")
    Collector().x(1, -1)
    assert repr(getter()) == expected

    Collector, getter = make_collector(examples.Simple, "two")
    Collector().x.run(1, -1)
    assert repr(getter()) == expected

    expected = (
        """
Proxy(SimpleSubstory.y):
  before
  x
    one
    two (skipped)
  after (returned: -4)
        """.strip()
    )

    Collector, getter = make_collector(examples.SimpleSubstory, "after")
    Collector().y(-2)
    assert repr(getter()) == expected

    Collector, getter = make_collector(examples.SimpleSubstory, "after")
    Collector().y.run(-2)
    assert repr(getter()) == expected

    expected = (
        """
Proxy(SubstoryDI.y):
  before
  x (Simple.x)
    one
    two (skipped)
  after (returned: -4)
        """.strip()
    )

    Collector, getter = make_collector(examples.SubstoryDI, "after")
    Collector(examples.Simple().x).y(-2)
    assert repr(getter()) == expected

    Collector, getter = make_collector(examples.SubstoryDI, "after")
    Collector(examples.Simple().x).y.run(-2)
    assert repr(getter()) == expected

    expected = (
        """
Proxy(SubstoryDI.y):
  before
  x (SimpleSubstory.z)
    first (skipped)
  after (returned: 4)
        """.strip()
    )

    Collector, getter = make_collector(examples.SubstoryDI, "after")
    Collector(examples.SimpleSubstory().z).y(2)
    assert repr(getter()) == expected

    Collector, getter = make_collector(examples.SubstoryDI, "after")
    Collector(examples.SimpleSubstory().z).y.run(2)
    assert repr(getter()) == expected

    # Error.

    expected = """
Proxy(StepError.x):
  one (errored: Exception)
    """.strip()

    Collector, getter = make_collector(examples.StepError, "one")
    with pytest.raises(Exception):
        Collector().x()
    assert repr(getter()) == expected

    Collector, getter = make_collector(examples.StepError, "one")
    with pytest.raises(Exception):
        Collector().x.run()
    assert repr(getter()) == expected
