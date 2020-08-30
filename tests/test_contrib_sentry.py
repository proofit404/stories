import pytest


@pytest.mark.xfail
def test_contrib_is_available():
    from stories.contrib.sentry.django import DjangoClient  # noqa: F401
