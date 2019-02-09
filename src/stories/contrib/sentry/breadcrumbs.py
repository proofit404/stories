"""
stories.contrib.sentry.breadcrumbs
----------------------------------

This module contains integration with Sentry.

:copyright: (c) 2018-2019 dry-python team.
:license: BSD, see LICENSE for more details.
"""

import stories._context
from raven.breadcrumbs import libraryhook, record


origin_context_init = stories._context.Context.__init__


@libraryhook("stories")
def track_context():
    def wrapper(ctx, ns, history):
        origin_context_init(ctx, ns, history)
        record(
            processor=lambda data: data.update(
                {"category": "story", "message": repr(ctx)}
            )
        )

    stories._context.Context.__init__ = wrapper
