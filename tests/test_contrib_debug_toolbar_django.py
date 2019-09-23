import pytest


pytest.importorskip("foo")
from stories.contrib.debug_toolbars.django import (  # isort:skip  # pragma: no cover  # noqa
    StoriesPanel,
)
