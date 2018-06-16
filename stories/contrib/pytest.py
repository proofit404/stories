import itertools

import stories._context
import stories._proxy
from _pytest.config import hookimpl


origin_context_init = stories._context.Context.__init__


def track_context(storage):
    def wrapper(ctx, ns, history=None):
        origin_context_init(ctx, ns, history=history)
        storage.append(ctx)

    return wrapper


@hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    storage = []
    stories._context.Context.__init__ = track_context(storage)
    yield
    stories._context.Context.__init__ = origin_context_init
    item.add_report_section(
        "call",
        "stories",
        "\n\n".join(
            itertools.chain.from_iterable(
                zip(
                    map(lambda ctx: "\n".join(ctx.history), storage), map(repr, storage)
                )
            )
        ),
    )
