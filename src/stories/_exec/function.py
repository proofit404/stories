from .._marker import Marker, substory_end, substory_start
from .._return import Failure, Result, Skip, Success
from .._wrap import BeginningOfStory, end_of_story


def execute(runner, ctx, methods, contract):

    skipped = 0

    for obj, method, protocol in methods:

        if skipped > 0:
            if method is end_of_story:
                skipped -= 1
            elif type(method) is BeginningOfStory:
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
            try:
                protocol.check_return_statement(obj, method, result.reason)
            except Exception as error:
                ctx.history.on_error(error.__class__.__name__)
                raise
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

        try:
            contract.check(obj, method, ctx, result.kwargs)
        except Exception as error:
            ctx.history.on_error(error.__class__.__name__)
            raise

        ctx.ns.update(result.kwargs)
        line = "Set by %s.%s" % (obj.__class__.__name__, method.__name__)
        ctx.lines.extend([line] * len(result.kwargs))

    return runner.finished()
