import pytest


pytest.importorskip("foo")
from stories.contrib.debug_toolbars.flask import (  # isort:skip  # pragma: no cover  # noqa
    StoriesPanel,
)
