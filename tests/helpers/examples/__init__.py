import pytest

import examples.methods  # noqa: F401


def contracts():
    import examples.contract_raw

    yield examples.contract_raw

    try:
        import examples.contract_pydantic

        yield examples.contract_pydantic
    except (SyntaxError, ImportError):
        pass

    try:
        import examples.contract_marshmallow

        yield examples.contract_marshmallow
    except ImportError:
        pass

    try:
        import examples.contract_cerberus

        yield examples.contract_cerberus
    except ImportError:
        pass


# Fixtures.


@pytest.fixture()
def c():
    import examples.context

    return examples.context


@pytest.fixture()
def f():
    import examples.failure_reasons

    return examples.failure_reasons


@pytest.fixture(params=contracts())
def m(request):
    return request.param
