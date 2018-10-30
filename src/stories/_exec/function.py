from .._collect import end_of_story
from .._marker import Marker, substory_end, substory_start
from .._return import Failure, Result, Skip, Success


def execute(runner, ctx, methods):

    skipped = 0

    for obj, method in methods:

        if skipped > 0:
            if method is end_of_story:
                skipped -= 1
            elif method.__name__ == "validate_substory_arguments":
                # FIXME: This is a really flaky comparison mechanism.
                skipped += 1
            continue

        ctx.history.before_call(method.__name__)

        try:
            result = method(obj, ctx)
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
            skipped = 1
            continue

        if result is substory_start:
            ctx.history.on_substory_start(method.method_name)
            continue

        if result is substory_end:
            ctx.history.on_substory_end()
            continue

        assert not set(ctx) & set(result.kwargs)
        ctx.ns.update(result.kwargs)
        line = "Set by %s.%s" % (obj.__class__.__name__, method.__name__)
        ctx.lines.extend([line] * len(result.kwargs))

    return runner.finished()
