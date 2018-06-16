import itertools

import pytest
import stories._context
import stories._proxy


origin_make_proxy = stories._proxy.make_proxy
origin_context_init = stories._context.Context.__init__


def track_proxy(storage):
    def wrapper(obj, ctx, history):

        proxy = origin_make_proxy(obj, ctx, history)
        storage[ctx.__position__][0] = proxy
        return proxy

    return wrapper


def track_context(storage, sequence):
    def wrapper(ctx, ns):

        origin_context_init(ctx, ns)
        position = next(sequence)
        ctx.__position__ = position
        storage[position] = [None, ctx]

    return wrapper


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    sequence = itertools.count()
    storage = {}
    stories._run.make_proxy = track_proxy(storage)
    stories._context.Context.__init__ = track_context(storage, sequence)
    yield
    stories._run.make_proxy = origin_make_proxy
    stories._context.Context.__init__ = origin_context_init
    item.add_report_section(
        "call",
        "stories",
        "\n\n".join(
            map(
                repr,
                filter(
                    None,
                    itertools.chain.from_iterable(
                        storage[i] for i in range(len(storage))
                    ),
                ),
            )
        ),
    )
