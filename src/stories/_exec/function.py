from .._marker import BeginningOfStory, EndOfStory
from .._return import Failure, Result, Skip, Success


def execute(runner, ctx, methods, contract):

    skipped = 0

    for method, protocol in methods:

        method_type = type(method)

        if skipped > 0:
            if method_type is EndOfStory:
                skipped -= 1
            elif method_type is BeginningOfStory:
                skipped += 1
            continue

        ctx.history.before_call(method.__name__)

        try:
            result = method(ctx)
        except Exception as error:
            ctx.history.on_error(error.__class__.__name__)
            raise

        restype = type(result)
        assert restype in (Result, Success, Failure, Skip)

        if restype is Failure:
            try:
                protocol.check_return_statement(method, result.reason)
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

        if method_type is BeginningOfStory:
            ctx.history.on_substory_start(method.method_name)
            continue

        if method_type is EndOfStory:
            ctx.history.on_substory_end()
            continue

        try:
            contract.check_success_statement(method, ctx, result.kwargs)
        except Exception as error:
            ctx.history.on_error(error.__class__.__name__)
            raise

        ctx.assign(method, result.kwargs)

    return runner.finished()
