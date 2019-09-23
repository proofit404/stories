import pytest


pytest.importorskip("foo")
from stories.contrib.sentry.django import (  # isort:skip  # pragma: no cover  # noqa
    DjangoClient,
)
