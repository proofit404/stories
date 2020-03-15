# -*- coding: utf-8 -*-
from debug_toolbar.panels import Panel
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy as __

import _stories.context
import _stories.mounted


# FIXME: Test me.


origin_make_context = _stories.context.make_context


def track_context(storage):
    def wrapper(contract, kwargs, history):
        ctx, ns, lines, bind = origin_make_context(contract, kwargs, history)
        storage.append(ctx)
        return ctx, ns, lines, bind

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
        _stories.mounted.make_context = track_context(self.storage)

    def disable_instrumentation(self):
        _stories.mounted.make_context = origin_make_context

    def generate_stats(self, request, response):
        self.record_stats({"stories": self.storage})  # FIXME: Use pretty print.
