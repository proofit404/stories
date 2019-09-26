# type: ignore
from flask import render_template
from flask_debugtoolbar.panels import DebugPanel

import _stories.context


# FIXME: Test me.
#
# FIXME: Type me.


original_context_init = _stories.context.Context.__init__


def track_context(storage):
    def wrapper(ctx):
        original_context_init(ctx)
        storage.append(ctx)

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
            "stories/debug_toolbar/stories_panel.html", stories=self.storage
        )

    def enable_instrumentation(self):
        _stories.context.Context.__init__ = track_context(self.storage)

    def disable_instrumentation(self):
        _stories.context.Context.__init__ = original_context_init
