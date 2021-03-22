"""Tests related to stub objects."""
from stories import I


def test_step_stub():
    """`I` object should not be usable outside of `Story` class."""
    assert I is None
