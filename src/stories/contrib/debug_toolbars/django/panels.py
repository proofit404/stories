"""
stories.contrib.debug_toolbars.django.panels
--------------------------------------------

This module contains integration with Django Debug Toolbar.

:copyright: (c) 2018-2019 dry-python team.
:license: BSD, see LICENSE for more details.
"""

import stories._context
from debug_toolbar.panels import Panel
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy as __


origin_context_init = stories._context.Context.__init__


def track_context(storage):
    def wrapper(ctx, ns, history):
        origin_context_init(ctx, ns, history)
        storage.append(ctx)

    return wrapper


class StoriesPanel(Panel):

    # Implement the Panel API

    template = "stories/debug_toolbar/stories_panel.html"

    nav_title = _("Stories")

    @property
    def nav_subtitle(self):
        count = len(self.storage)
        return __("%(count)d call", "%(count)d calls", count) % {"count": count}

    @property
    def title(self):
        count = len(self.storage)
        return __(
            "Context and execution path of %(count)d story",
            "Context and execution path of %(count)d stories",
            count,
        ) % {"count": count}

    # Implement the Collector.

    def __init__(self, *args, **kwargs):
        super(StoriesPanel, self).__init__(*args, **kwargs)
        self.storage = []

    def enable_instrumentation(self):
        stories._context.Context.__init__ = track_context(self.storage)

    def disable_instrumentation(self):
        stories._context.Context.__init__ = origin_context_init

    def generate_stats(self, request, response):
        self.record_stats({"stories": self.storage})
