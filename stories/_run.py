import sys

from ._collect import end_of_story
from ._context import Context
from ._marker import Undefined, undefined, valid_arguments
from ._return import Failure, Result, Skip, Success
from ._summary import FailureSummary, SuccessSummary
from .exceptions import FailureError


def tell_the_story(cls_name, name, methods, arguments, args, kwargs):

    ctx = Context(validate_arguments(arguments, args, kwargs))
    skipped = undefined
    history = ["Proxy(" + cls_name + "." + name + "):"]
    indent_level = 1

    for self, method, of in methods:

        if skipped is not undefined:
            if method is end_of_story and skipped is of:
                skipped = undefined
            continue

        history.append("  " * indent_level + method.__name__)
        try:
            result = method(make_proxy(self, ctx, history))
        except Exception as error:
            history[-1] = history[-1] + " (errored: " + error.__class__.__name__ + ")"
            raise

        restype = type(result)
        assert restype in (Result, Success, Failure, Skip, Undefined)

        if restype is Failure:
            if result.reason:
                history[-1] = history[-1] + " (failed: " + repr(result.reason) + ")"
            else:
                history[-1] = history[-1] + " (failed)"
            raise FailureError(result.reason)

        if restype is Result:
            history[-1] = history[-1] + " (returned: " + repr(result.value) + ")"
            return result.value

        if restype is Skip:
            history[-1] = history[-1] + " (skipped)"
            skipped = of
            # Substory will be skipped.
            indent_level -= 1
            continue

        if restype is Undefined:
            history.pop()
            if result is valid_arguments:
                # The beginning of substory.
                history.append("  " * indent_level + method.method_name)
                indent_level += 1
            else:
                # The end of substory.
                indent_level -= 1
            continue

        assert not set(ctx.ns) & set(result.kwargs)
        ctx.ns.update(result.kwargs)
        line = "Set by %s.%s" % (self.__class__.__name__, method.__name__)
        ctx.lines.extend([(key, line) for key in result.kwargs])


def run_the_story(cls_name, name, methods, arguments, args, kwargs):

    ctx = Context(validate_arguments(arguments, args, kwargs))
    skipped = undefined
    history = ["Proxy(" + cls_name + "." + name + "):"]
    indent_level = 1

    for self, method, of in methods:

        if skipped is not undefined:
            if method is end_of_story and skipped is of:
                skipped = undefined
            continue

        history.append("  " * indent_level + method.__name__)
        result = method(make_proxy(self, ctx, history))

        restype = type(result)
        assert restype in (Result, Success, Failure, Skip, Undefined)

        if restype is Failure:
            if result.reason:
                history[-1] = history[-1] + " (failed: " + repr(result.reason) + ")"
            else:
                history[-1] = history[-1] + " (failed)"
            return FailureSummary(ctx, method.__name__, result.reason)

        if restype is Result:
            history[-1] = history[-1] + " (returned: " + repr(result.value) + ")"
            return SuccessSummary(result.value)

        if restype is Skip:
            history[-1] = history[-1] + " (skipped)"
            skipped = of
            # Substory will be skipped.
            indent_level -= 1
            continue

        if restype is Undefined:
            history.pop()
            if result is valid_arguments:
                # The beginning of substory.
                history.append("  " * indent_level + method.method_name)
                indent_level += 1
            else:
                # The end of substory.
                indent_level -= 1
            continue

        assert not set(ctx.ns) & set(result.kwargs)
        ctx.ns.update(result.kwargs)
        line = "Set by %s.%s" % (self.__class__.__name__, method.__name__)
        ctx.lines.extend([(key, line) for key in result.kwargs])

    return SuccessSummary(None)


def validate_arguments(arguments, args, kwargs):

    assert not (args and kwargs)

    if args:
        assert len(arguments) == len(args)
        return {k: v for k, v in zip(arguments, args)}

    assert set(arguments) == set(kwargs)
    return kwargs


PY3 = sys.version_info[0] >= 3


if PY3:

    def make_proxy(obj, ctx, history):
        return Proxy(obj, ctx, history)


else:

    def make_proxy(obj, ctx, history):
        class ObjectProxy(Proxy, obj.__class__):
            pass

        return ObjectProxy(obj, ctx, history)


class Proxy(object):
    def __init__(self, obj, ctx, history):
        self.obj = obj
        self.ctx = ctx
        self.history = history

    def __getattr__(self, name):
        return getattr(self.obj, name)

    def __repr__(self):
        return "\n".join(self.history)
