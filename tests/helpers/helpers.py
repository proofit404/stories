import configparser

import _stories.context


def make_collector():
    # FIXME: Rewrite to the context manager.  Disable instrumentation
    # on exit.

    storage = []

    origin_context_init = _stories.context.Context.__init__

    def wrapper(ctx):
        origin_context_init(ctx)
        storage.append(ctx)

    _stories.context.Context.__init__ = wrapper

    def getter():
        length = len(storage)
        error_message = "Context() was called {length} times".format(length=length)
        assert length == 1, error_message
        return storage[0]

    return getter


def get_tox_deps():
    ini_parser = configparser.ConfigParser()
    ini_parser.read("tox.ini")
    for section in ini_parser:
        if "deps" in ini_parser[section]:
            deps = ini_parser[section]["deps"].strip().splitlines()
            yield deps
