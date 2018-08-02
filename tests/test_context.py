import pytest
from stories._context import Context


def test_expand_context():
    """
    We can expand context to the function call arguments without too
    much boilerplate.
    """

    func = lambda foo, bar, baz: foo + bar + baz  # noqa: E731

    ctx = Context({"foo": 1, "bar": 2, "baz": 3})

    assert func(**ctx("foo", "bar", "baz")) == 6

    ctx = Context({"one": 1, "two": 2, "three": 3})

    assert func(**ctx(foo="one", bar="two", baz="three")) == 6

    with pytest.raises(AssertionError):
        ctx("one", one="two")
