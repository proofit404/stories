"""
stories.contrib.sentry.breadcrumbs
----------------------------------

This module contains integration with Sentry.

:copyright: (c) 2018-2019 dry-python team.
:license: BSD, see LICENSE for more details.
"""

from raven.breadcrumbs import libraryhook, record

import stories._context
from stories._types import AbstractContext


origin_context_init = stories._context.Context.__init__


@libraryhook("stories")
def track_context():
    # type: () -> None
    def wrapper(ctx):
        # type: (AbstractContext) -> None
        origin_context_init(ctx)
        record(
            processor=lambda data: data.update(
                {"category": "story", "message": repr(ctx)}
            )
        )

    stories._context.Context.__init__ = wrapper
