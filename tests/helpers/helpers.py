import _stories.context
import _stories.mounted


origin_make_context = _stories.context.make_context


def make_collector():
    # FIXME: Rewrite to the context manager.  Disable instrumentation
    # on exit.

    storage = []

    def wrapper(contract, kwargs, history):
        ctx, ns, lines, set_method = origin_make_context(contract, kwargs, history)
        storage.append(ctx)
        return ctx, ns, lines, set_method

    _stories.mounted.make_context = wrapper

    def getter():
        length = len(storage)
        error_message = f"Context() was called {length} times"
        assert length == 1, error_message
        return storage[0]

    return getter
