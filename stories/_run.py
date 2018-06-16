from ._collect import end_of_story
from ._marker import Marker, substory_end, substory_start, undefined
from ._return import Failure, Result, Skip, Success
from ._summary import FailureSummary, SuccessSummary
from .exceptions import FailureError


def tell_the_story(ctx, history, methods):

    skipped = undefined
    indent_level = 1

    for proxy, method in methods:

        if skipped is not undefined:
            if method is end_of_story and skipped is proxy:
                skipped = undefined
            continue

        history.append("  " * indent_level + method.__name__)

        try:
            try:
                result = method(proxy)
            except AttributeError as error:
                if proxy.__class__.__name__ in error.args[0]:
                    assert False
                else:
                    raise
        except Exception as error:
            history[-1] = history[-1] + " (errored: " + error.__class__.__name__ + ")"
            raise

        restype = type(result)
        assert restype in (Result, Success, Failure, Skip, Marker)

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
            skipped = proxy
            # Substory will be skipped.
            indent_level -= 1
            continue

        if result is substory_start:
            history.pop()
            history.append("  " * indent_level + method.method_name)
            indent_level += 1
            continue

        if result is substory_end:
            history.pop()
            indent_level -= 1
            continue

        assert not set(ctx) & set(result.kwargs)
        ctx.ns.update(result.kwargs)
        line = "Set by %s.%s" % (proxy.__class__.__name__, method.__name__)
        ctx.lines.extend([line] * len(result.kwargs))


def run_the_story(ctx, history, methods):

    skipped = undefined
    indent_level = 1

    for proxy, method in methods:

        if skipped is not undefined:
            if method is end_of_story and skipped is proxy:
                skipped = undefined
            continue

        history.append("  " * indent_level + method.__name__)

        try:
            try:
                result = method(proxy)
            except AttributeError as error:
                if proxy.__class__.__name__ in error.args[0]:
                    assert False
                else:
                    raise
        except Exception as error:
            history[-1] = history[-1] + " (errored: " + error.__class__.__name__ + ")"
            raise

        restype = type(result)
        assert restype in (Result, Success, Failure, Skip, Marker)
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
            skipped = proxy
            # Substory will be skipped.
            indent_level -= 1
            continue

        if result is substory_start:
            history.pop()
            history.append("  " * indent_level + method.method_name)
            indent_level += 1
            continue

        if result is substory_end:
            history.pop()
            indent_level -= 1
            continue

        assert not set(ctx) & set(result.kwargs)
        ctx.ns.update(result.kwargs)
        line = "Set by %s.%s" % (proxy.__class__.__name__, method.__name__)
        ctx.lines.extend([line] * len(result.kwargs))

    return SuccessSummary(None)
