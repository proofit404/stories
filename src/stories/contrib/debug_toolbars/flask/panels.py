"""
stories.contrib.debug_toolbars.flask.panels
-------------------------------------------

This module contains integration with flask-debugtoolbar.

:copyright: (c) 2018-2019 dry-python team.
:license: BSD, see LICENSE for more details.
"""

from typing import Callable, Dict, List, Optional, Union

from flask import render_template
from flask_debugtoolbar.panels import DebugPanel
from jinja2 import Environment

import stories._context
from stories._types import AbstractContext


original_context_init = stories._context.Context.__init__


TemplateContext = Dict[str, str]
PanelArgument = Union[Environment, TemplateContext]


def track_context(storage):
    # type: (List[AbstractContext]) -> Callable[[AbstractContext], None]
    def wrapper(ctx):
        # type: (AbstractContext) -> None
        original_context_init(ctx)
        storage.append(ctx)

    return wrapper


def pluralize(number, singular, plural=None):
    # type: (int, str, Optional[str]) -> str
    if plural is None:
        plural = singular + "s"
    if number == 1:
        return "%d %s" % (number, singular)
    else:
        return "%d %s" % (number, plural)


class StoriesPanel(DebugPanel):
    name = "Stories"
    has_content = True

    def __init__(self, *args, **kwargs):
        # type: (*PanelArgument, **PanelArgument) -> None
        DebugPanel.__init__(self, *args, **kwargs)
        self.storage = []  # type: List[AbstractContext]
        self.enable_instrumentation()

    def nav_title(self):
        # type: () -> str
        return "Stories"

    def nav_subtitle(self):
        # type: () -> str
        count = len(self.storage)
        return pluralize(count, "call")

    def title(self):
        # type: () -> str
        count = len(self.storage)
        return "Context and execution path of %s" % pluralize(count, "story", "stories")

    def url(self):
        # type: () -> str
        return "#"

    def content(self):
        # type: () -> str
        return render_template(
            "stories/debug_toolbar/stories_panel.html", stories=self.storage
        )

    def enable_instrumentation(self):
        # type: () -> None
        stories._context.Context.__init__ = track_context(self.storage)  # type: ignore

    def disable_instrumentation(self):
        # type: () -> None
        stories._context.Context.__init__ = original_context_init  # type: ignore
