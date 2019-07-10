"""
stories.contrib.debug_toolbars.django.panels
--------------------------------------------

This module contains integration with Django Debug Toolbar.

:copyright: (c) 2018-2019 dry-python team.
:license: BSD, see LICENSE for more details.
"""

from typing import Callable, List, Union

from debug_toolbar.panels import Panel
from debug_toolbar.toolbar import DebugToolbar
from django.http import HttpRequest, HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy as __

import stories._context
from stories._types import AbstractContext


origin_context_init = stories._context.Context.__init__


GetResponse = Callable[[HttpRequest], HttpResponse]
PanelArgument = Union[DebugToolbar, GetResponse]


def track_context(storage):
    # type: (List[AbstractContext]) -> Callable[[AbstractContext], None]
    def wrapper(ctx):
        # type: (AbstractContext) -> None
        origin_context_init(ctx)
        storage.append(ctx)

    return wrapper


class StoriesPanel(Panel):

    # Implement the Panel API

    template = "stories/debug_toolbar/stories_panel.html"

    nav_title = _("Stories")

    @property
    def nav_subtitle(self):
        # type: () -> str
        count = len(self.storage)
        return __("%(count)d call", "%(count)d calls", count) % {"count": count}

    @property
    def title(self):
        # type: () -> str
        count = len(self.storage)
        return __(
            "Context and execution path of %(count)d story",
            "Context and execution path of %(count)d stories",
            count,
        ) % {"count": count}

    # Implement the Collector.

    def __init__(self, *args, **kwargs):
        # type: (*PanelArgument, **PanelArgument) -> None
        super(StoriesPanel, self).__init__(*args, **kwargs)
        self.storage = []  # type: List[AbstractContext]

    def enable_instrumentation(self):
        # type: () -> None
        stories._context.Context.__init__ = track_context(self.storage)  # type: ignore

    def disable_instrumentation(self):
        # type: () -> None
        stories._context.Context.__init__ = origin_context_init  # type: ignore

    def generate_stats(self, request, response):
        # type: (HttpRequest, HttpResponse) -> None
        self.record_stats({"stories": self.storage})
