# type: ignore
from raven.breadcrumbs import libraryhook
from raven.breadcrumbs import record

import _stories.context


# FIXME: Test me.
#
# FIXME: Type me.


origin_context_init = _stories.context.Context.__init__


@libraryhook("stories")
def track_context():
    def wrapper(ctx):
        origin_context_init(ctx)
        record(
            processor=lambda data: data.update(
                {"category": "story", "message": repr(ctx)}
            )
        )

    _stories.context.Context.__init__ = wrapper
