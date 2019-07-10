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
from typing import Callable, Iterable, List, Tuple

from _pytest.config import hookimpl
from _pytest.nodes import Item

import stories._compat
import stories._context
from stories._types import AbstractContext


origin_context_init = stories._context.Context.__init__


def track_context(storage):
    # type: (List[Tuple[str, AbstractContext]]) -> Callable[[AbstractContext], None]
    def wrapper(ctx):
        # type: (AbstractContext) -> None
        origin_context_init(ctx)
        storage.append((get_test_source(*get_test_call()), ctx))

    return wrapper


def get_test_call():
    # type: () -> Tuple[str, int]
    f = sys._getframe()

    while True:
        if (
            "@py_builtins" in f.f_globals
            and "@pytest_ar" in f.f_globals
            and f.f_code.co_filename != __file__
        ):
            return f.f_code.co_filename, f.f_lineno
        elif not f.f_back:
            raise Exception("Can not find running test")
        else:
            f = f.f_back


def get_test_source(filename, lineno):
    # type: (str, int) -> str
    start = max(1, lineno - 3)
    end = lineno + 3
    adjust_to = len(str(end))

    lines = [linecache.getline(filename, no) for no in range(start, end)]
    text = textwrap.dedent("".join(lines))

    src = []
    for num, line in zip(range(start, end), text.splitlines()):
        sep = "->" if num == lineno else "  "
        src.append((" %s %s %s" % (str(num).rjust(adjust_to), sep, line)).rstrip())

    return "\n".join(src)


@hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    # type: (Item) -> Iterable[None]
    storage = []  # type: List[Tuple[str, AbstractContext]]
    stories._context.Context.__init__ = track_context(storage)  # type: ignore
    yield
    stories._context.Context.__init__ = origin_context_init  # type: ignore
    for i, (src, ctx) in enumerate(storage, 1):
        output = "\n\n".join(
            [
                src,
                stories._context.history_representation(ctx)
                + "\n\n"
                + stories._context.context_representation(ctx, stories._compat.pformat),
            ]
        )
        item.add_report_section("call", "story #%d" % (i,), output)
