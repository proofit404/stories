import pytest

import examples
from stories.exceptions import ContextContractError


def test_arguments_validation():

    with pytest.raises(AssertionError):
        examples.methods.Simple().x(1)

    with pytest.raises(AssertionError):
        examples.methods.Simple().x.run(1)

    with pytest.raises(AssertionError):
        examples.methods.Simple().x(1, b=2)

    with pytest.raises(AssertionError):
        examples.methods.Simple().x.run(1, b=2)


def test_context_immutability():

    expected = """
This variables already present in the context: 'bar', 'foo'

Function returned value: ExistedKey.one

Use different names for Success() keyword arguments.
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        examples.contract.ExistedKey().x(1, 2)
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        examples.contract.ExistedKey().x.run(1, 2)
    assert str(exc_info.value) == expected

    # Substory inheritance.

    expected = """
This variables already present in the context: 'bar', 'foo'

Function returned value: SubstoryExistedKey.one

Use different names for Success() keyword arguments.
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        examples.contract.SubstoryExistedKey().a(1, 2)
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        examples.contract.SubstoryExistedKey().a.run(1, 2)
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
This variables already present in the context: 'bar', 'foo'

Function returned value: ExistedKey.one

Use different names for Success() keyword arguments.
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        examples.contract.ExistedKeyDI().a(1, 2)
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        examples.contract.ExistedKeyDI().a.run(1, 2)
    assert str(exc_info.value) == expected
