# -*- coding: utf-8 -*-
from _stories.marker import BeginningOfStory
from _stories.marker import EndOfStory
from _stories.returned import Failure
from _stories.returned import Result
from _stories.returned import Skip
from _stories.returned import Success


async def execute(runner, ctx, ns, bind, history, methods):
    __tracebackhide__ = True

    skipped = 0

    for method, contract, protocol in methods:

        method_type = type(method)

        if skipped > 0:
            if method_type is EndOfStory:
                skipped -= 1
            elif method_type is BeginningOfStory:
                skipped += 1
            continue

        if method_type is BeginningOfStory:
            history.on_substory_start(method.story_name)
            try:
                contract.check_substory_call(ctx, ns)
            except Exception as error:
                history.on_error(error.__class__.__name__)
                raise
            continue

        if method_type is EndOfStory:
            history.on_substory_end()
            continue

        history.before_call(method.__name__)
        bind(contract, method)

        try:
            result = await method(ctx)
        except Exception as error:
            history.on_error(error.__class__.__name__)
            raise

        restype = type(result)
        if restype not in (Result, Success, Failure, Skip):
            raise AssertionError

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

    return runner.finished()
