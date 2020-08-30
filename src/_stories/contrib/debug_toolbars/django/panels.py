from debug_toolbar.panels import Panel

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
    template = "stories/debug_toolbar/stories_panel.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.storage = []

    @property
    def nav_title(self):
        return "Stories"

    @property
    def nav_subtitle(self):
        count = len(self.storage)
        template = "%(count)d call" if count == 1 else "%(count)d calls"
        return template % {"count": count}

    @property
    def title(self):
        count = len(self.storage)
        template = (
            "Context and execution path of %(count)d story"
            if count == 1
            else "Context and execution path of %(count)d stories"
        )
        return template % {"count": count}

    def enable_instrumentation(self):
        _stories.mounted.make_context = track_context(self.storage)

    def disable_instrumentation(self):
        _stories.mounted.make_context = origin_make_context

    def generate_stats(self, request, response):
        self.record_stats({"stories": self.storage})  # FIXME: Use pretty print.
