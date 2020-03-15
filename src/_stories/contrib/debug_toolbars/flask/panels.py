# -*- coding: utf-8 -*-
from flask import render_template
from flask_debugtoolbar.panels import DebugPanel

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


def pluralize(number, singular, plural=None):
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
        super(StoriesPanel, self).__init__(*args, **kwargs)
        self.storage = []
        self.enable_instrumentation()

    def nav_title(self):
        return "Stories"

    def nav_subtitle(self):
        count = len(self.storage)
        return pluralize(count, "call")

    def title(self):
        count = len(self.storage)
        return "Context and execution path of %s" % pluralize(count, "story", "stories")

    def url(self):
        return "#"

    def content(self):
        return render_template(
            "stories/debug_toolbar/stories_panel.html",
            stories=self.storage,  # FIXME: Use pretty print.
        )

    def enable_instrumentation(self):
        _stories.mounted.make_context = track_context(self.storage)

    def disable_instrumentation(self):
        _stories.mounted.make_context = origin_make_context
