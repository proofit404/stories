import stories._context


origin_context_init = stories._context.Context.__init__


def make_collector():

    storage = []

    def wrapper(ctx, ns, history, contract):
        origin_context_init(ctx, ns, history, contract)
        storage.append(ctx)

    stories._context.Context.__init__ = wrapper

    def getter():
        length = len(storage)
        error_message = "Context() was called {length} times".format(length=length)
        assert length == 1, error_message
        return storage[0]

    return getter
