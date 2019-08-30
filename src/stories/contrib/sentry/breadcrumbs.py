# type: ignore
"""
stories.contrib.sentry.breadcrumbs
----------------------------------

This module contains integration with Sentry.

:copyright: (c) 2018-2019 dry-python team.
:license: BSD, see LICENSE for more details.
"""

from raven.breadcrumbs import libraryhook, record

import stories._context


# FIXME: Test me.
#
# FIXME: Type me.


origin_context_init = stories._context.Context.__init__


@libraryhook("stories")
def track_context():
    def wrapper(ctx):
        origin_context_init(ctx)
        record(
            processor=lambda data: data.update(
                {"category": "story", "message": repr(ctx)}
            )
        )

    stories._context.Context.__init__ = wrapper
