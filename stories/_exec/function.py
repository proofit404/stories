from .._collect import end_of_story
from .._marker import Marker, substory_end, substory_start, undefined
from .._return import Failure, Result, Skip, Success


def execute(runner, ctx, methods):

    skipped = undefined

    for proxy, method in methods:

        if skipped is not undefined:
            if method is end_of_story and skipped is proxy:
                skipped = undefined
            continue

        ctx.history.before_call(method.__name__)

        try:
            try:
                # FIXME:
                #
                # 1. We should get away from proxy system.
                #
                # 2. Context should show current execution path.
                result = method(proxy, ctx)
            except AttributeError as error:
                if proxy.__class__.__name__ in error.args[0]:
                    assert False
                else:
                    raise
        except Exception as error:
            ctx.history.on_error(error.__class__.__name__)
            raise

        restype = type(result)
        assert restype in (Result, Success, Failure, Skip, Marker)

        if restype is Failure:
            ctx.history.on_failure(result.reason)
            return runner.got_failure(ctx, method.__name__, result.reason)

        if restype is Result:
            ctx.history.on_result(result.value)
            return runner.got_result(result.value)

        if restype is Skip:
            ctx.history.on_skip()
            skipped = proxy
            continue

        if result is substory_start:
            ctx.history.on_substory_start(method.method_name)
            continue

        if result is substory_end:
            ctx.history.on_substory_end()
            continue

        assert not set(ctx) & set(result.kwargs)
        ctx.ns.update(result.kwargs)
        line = "Set by %s.%s" % (proxy.__class__.__name__, method.__name__)
        ctx.lines.extend([line] * len(result.kwargs))

    return runner.finished()
