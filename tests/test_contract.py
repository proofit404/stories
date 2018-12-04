import pytest

import examples
from stories.exceptions import ContextContractError


def test_context_immutability():

    # TODO: Check the same method with
    #
    # [ ] Inheritance substories.
    #
    # [ ] Substories DI.

    expected = """
This variables already present in the context: 'bar', 'foo'

Function returned value: ExistedKey.one

Use different names as Success() arguments.
""".strip()

    with pytest.raises(ContextContractError) as exc_info:
        examples.contract.ExistedKey().x(1, 2)
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        examples.contract.ExistedKey().x.run(1, 2)
    assert str(exc_info.value) == expected
