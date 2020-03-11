# -*- coding: utf-8 -*-
# type: ignore
from raven.breadcrumbs import libraryhook
from raven.breadcrumbs import record

import _stories.context
import _stories.mounted


# FIXME: Test me.
#
# FIXME: Type me.


origin_make_context = _stories.context.make_context


@libraryhook("stories")
def track_context():
    def wrapper(contract, kwargs, history):
        ctx, ns, lines = origin_make_context(contract, kwargs, history)
        record(
            processor=lambda data: data.update(
                {"category": "story", "message": repr(ctx)}  # FIXME: Use pretty print.
            )
        )
        return ctx, ns, lines

    _stories.mounted.make_context = wrapper
