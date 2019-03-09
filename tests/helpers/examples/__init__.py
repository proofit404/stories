import pytest

import examples.context
import examples.contract_raw
import examples.failure_reasons
import examples.methods
import examples.shortcuts


contracts = [examples.contract_raw]


try:
    import examples.contract_pydantic

    contracts.append(examples.contract_pydantic)
except (SyntaxError, ImportError):
    pass

try:
    import examples.contract_marshmallow

    contracts.append(examples.contract_marshmallow)
except ImportError:
    pass

try:
    import examples.contract_cerberus

    contracts.append(examples.contract_cerberus)
except ImportError:
    pass


# Fixtures.


@pytest.fixture
def c():
    return examples.context


@pytest.fixture
def f():
    return examples.failure_reasons


@pytest.fixture(params=contracts)
def m(request):
    return request.param
