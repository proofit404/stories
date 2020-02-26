# -*- coding: utf-8 -*-
import configparser
import textwrap

import _stories.context
import _stories.mounted


origin_make_context = _stories.context.make_context


def make_collector():
    # FIXME: Rewrite to the context manager.  Disable instrumentation
    # on exit.

    storage = []

    def wrapper(contract, kwargs, history):
        ctx, ns, lines = origin_make_context(contract, kwargs, history)
        storage.append(ctx)
        return ctx, ns, lines

    _stories.mounted.make_context = wrapper

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
