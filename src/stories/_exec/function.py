from .._context import assign_namespace
from .._marker import BeginningOfStory, EndOfStory
from .._return import Failure, Result, Skip, Success


def execute(runner, ctx, history, methods):

    skipped = 0

    for method, contract, protocol in methods:

        method_type = type(method)

        if skipped > 0:
            if method_type is EndOfStory:
                skipped -= 1
            elif method_type is BeginningOfStory:
                skipped += 1
            continue

        history.before_call(method.__name__)

        try:
            result = method(ctx)
        except Exception as error:
            history.on_error(error.__class__.__name__)
            raise

        restype = type(result)
        assert restype in (Result, Success, Failure, Skip)

        if restype is Failure:
            try:
                protocol.check_return_statement(method, result.reason)
            except Exception as error:
                history.on_error(error.__class__.__name__)
                raise
            history.on_failure(result.reason)
            return runner.got_failure(ctx, method.__name__, result.reason)

        if restype is Result:
            history.on_result(result.value)
            return runner.got_result(result.value)

        if restype is Skip:
            history.on_skip()
            skipped = 1
            continue

        if method_type is BeginningOfStory:
            try:
                contract.check_story_arguments(ctx)
            except Exception as error:
                history.on_error(error.__class__.__name__)
                raise
            history.on_substory_start()
            continue

        if method_type is EndOfStory:
            history.on_substory_end()
            continue

        try:
            contract.check_success_statement(method, ctx, result.kwargs)
        except Exception as error:
            history.on_error(error.__class__.__name__)
            raise

        assign_namespace(ctx, method, result.kwargs)

    return runner.finished()
