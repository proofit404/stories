"""Tests related to story arguments."""
from stories import Argument


def test_placeholder():
    """Verify Argument placeholder."""
    argument = Argument()
    assert argument.validate is None
    argument = Argument(lambda: 1)
    assert argument.validate() == 1
