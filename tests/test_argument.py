import functools

import pytest

from stories._argument import argument


@pytest.mark.parametrize(
    ("decors", "expected"),
    [
        ([argument("foo")], ["foo"]),
        ([argument("foo", "bar")], ["bar", "foo"]),
        ([argument("foo"), argument("bar")], ["bar", "foo"]),
        ((argument("foo", "baz"), argument("bar")), ["bar", "baz", "foo"]),
    ],
)
def test_argument(decors, expected):
    def foo():
        pass

    foo = functools.reduce(lambda func, deco: deco(func), decors, foo)

    assert hasattr(foo, "arguments")
    assert foo.arguments == expected
