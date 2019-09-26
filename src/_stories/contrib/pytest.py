# type: ignore
import linecache
import sys
import textwrap

from _pytest.config import hookimpl

import _stories.compat
import _stories.context


# FIXME: Test me.
#
# FIXME: Type me.


origin_context_init = _stories.context.Context.__init__


def track_context(storage):
    def wrapper(ctx):
        origin_context_init(ctx)
        storage.append((get_test_source(*get_test_call()), ctx))

    return wrapper


def get_test_call():
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
    _stories.context.Context.__init__ = track_context(storage)
    yield
    _stories.context.Context.__init__ = origin_context_init
    for i, (src, ctx) in enumerate(storage, 1):
        output = "\n\n".join(
            [
                src,
                _stories.context.history_representation(ctx)
                + "\n\n"
                + _stories.context.context_representation(ctx, _stories.compat.pformat),
            ]
        )
        item.add_report_section("call", "story #%d" % (i,), output)
