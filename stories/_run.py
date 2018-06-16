from ._collect import end_of_story
from ._context import Context
from ._marker import Undefined, undefined, valid_arguments
from ._return import Failure, Result, Skip, Success
from ._summary import FailureSummary, SuccessSummary
from .exceptions import FailureError


def tell_the_story(cls_name, name, methods, arguments, args, kwargs):

    ctx = Context(validate_arguments(arguments, args, kwargs))
    proxy = current_self = skipped = undefined
    history = ["Proxy(" + cls_name + "." + name + "):"]
    indent_level = 1

    for self, method, of in methods:

        if skipped is not undefined:
            if method is end_of_story and skipped is of:
                skipped = undefined
            continue

        if current_self is not self:
            proxy = make_proxy(self, ctx, history)
            current_self = self

        history.append("  " * indent_level + method.__name__)
        try:
            result = method(proxy)
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
        ctx.lines.extend([line] * len(result.kwargs))


def run_the_story(cls_name, name, methods, arguments, args, kwargs):

    ctx = Context(validate_arguments(arguments, args, kwargs))
    proxy = current_self = skipped = undefined
    history = ["Proxy(" + cls_name + "." + name + "):"]
    indent_level = 1

    for self, method, of in methods:

        if skipped is not undefined:
            if method is end_of_story and skipped is of:
                skipped = undefined
            continue

        if current_self is not self:
            proxy = make_proxy(self, ctx, history)
            current_self = self

        history.append("  " * indent_level + method.__name__)
        try:
            result = method(proxy)
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
        ctx.lines.extend([line] * len(result.kwargs))

    return SuccessSummary(None)


def validate_arguments(arguments, args, kwargs):

    assert not (args and kwargs)

    if args:
        assert len(arguments) == len(args)
        return [(k, v) for k, v in zip(arguments, args)]

    assert set(arguments) == set(kwargs)
    return [(k, kwargs[k]) for k in arguments]


def make_proxy(obj, ctx, history):
    class Proxy:
        def __repr__(self):
            return "\n".join(history)

    proxy = Proxy()
    # TODO: Support slots.
    for name, attr in obj.__dict__.items():
        setattr(proxy, name, attr)
    proxy.ctx = ctx
    return proxy
