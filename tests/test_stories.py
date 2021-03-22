"""Tests related to stories module."""
from stories.exceptions import StoryError


def test_exception():
    """`StoryError` should be Exception subclass."""
    assert issubclass(StoryError, Exception)
