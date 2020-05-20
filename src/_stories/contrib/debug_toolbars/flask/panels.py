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


class StoriesPanel(DebugPanel):
    name = "Stories"
    has_content = True
    template = "stories/debug_toolbar/stories_panel.html"

    def __init__(self, *args, **kwargs):
        super(StoriesPanel, self).__init__(*args, **kwargs)
        self.storage = []
        self.enable_instrumentation()

    def nav_title(self):
        return "Stories"

    def nav_subtitle(self):
        count = len(self.storage)
        template = "%(count)d call" if count == 1 else "%(count)d calls"
        return template % {"count": count}

    def title(self):
        count = len(self.storage)
        template = (
            "Context and execution path of %(count)d story"
            if count == 1
            else "Context and execution path of %(count)d stories"
        )
        return template % {"count": count}

    def url(self):
        return "#"

    def enable_instrumentation(self):
        _stories.mounted.make_context = track_context(self.storage)

    def disable_instrumentation(self):
        _stories.mounted.make_context = origin_make_context

    def content(self):
        # FIXME: Use pretty print.
        return render_template(self.template, stories=self.storage)
