import configparser
import textwrap

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


def tox_info(var):
    """Get variable value from all sections in the tox.ini file."""
    ini_parser = configparser.ConfigParser()
    ini_parser.read("tox.ini")
    for section in ini_parser:
        if var in ini_parser[section]:
            value = textwrap.dedent(ini_parser[section][var].strip())
            yield section, value
