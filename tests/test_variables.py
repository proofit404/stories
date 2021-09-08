"""Tests related to story variables."""
from stories import Variable


def test_placeholder():
    """Verify Variable placeholder."""
    variable = Variable()
    assert variable.validate is None
    variable = Variable(lambda: 1)
    assert variable.validate() == 1
