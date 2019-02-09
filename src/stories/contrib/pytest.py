"""
stories.contrib.pytest
----------------------

This module contains integration with PyTest framework.

:copyright: (c) 2018-2019 dry-python team.
:license: BSD, see LICENSE for more details.
"""

import linecache
import sys
import textwrap

from _pytest.config import hookimpl

import stories._context


origin_context_init = stories._context.Context.__init__


def track_context(storage):
    def wrapper(ctx, ns, history):
        origin_context_init(ctx, ns, history)
        storage.append((get_test_source(*get_test_call()), ctx))

    return wrapper


def get_test_call():
    f = sys._getframe()

    while True:
        if (
            "@py_builtins" in f.f_globals
            and "@pytest_ar" in f.f_globals
            and f.f_code.co_name.startswith("test_")
            and f.f_code.co_filename != __file__
        ):
            return f.f_code.co_filename, f.f_lineno
        elif not f.f_back:
            raise Exception("Can not find running test")
        else:
            f = f.f_back


def get_test_source(filename, lineno):

    start = max(1, lineno - 3)
    end = lineno + 3
    adjust_to = len(str(end))

    lines = [linecache.getline(filename, no) for no in range(start, end)]
    text = textwrap.dedent("".join(lines))

    src = []
    for num, line in zip(range(start, end), text.splitlines()):
        sep = "->" if num == lineno else "  "
        src.append((" %s %s %s" % (str(num).rjust(adjust_to), sep, line)).rstrip())
    src = "\n".join(src)

    return src


@hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    storage = []
    stories._context.Context.__init__ = track_context(storage)
    yield
    stories._context.Context.__init__ = origin_context_init
    for i, (src, ctx) in enumerate(storage, 1):
        output = "\n\n".join([src, repr(ctx)])
        item.add_report_section("call", "story #%d" % (i,), output)
