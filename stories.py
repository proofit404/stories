"""
stories
-------

This module implements Business Transaction DSL.

:copyright: (c) 2018 by Artem Malyshev.
:license: BSD, see LICENSE for more details.
"""


__all__ = ["story", "argument", "Result", "Success", "Failure"]


undefined = object()


def story(f):

    def wrapper(self, *args, **kwargs):
        assert not (args and kwargs)
        arguments = getattr(f, "arguments", [])
        if args:
            assert len(arguments) == len(args)
            kwargs = {k: v for k, v in zip(arguments, args)}
        else:
            assert set(arguments) == set(kwargs)
        proxy = Proxy(self, Context(kwargs))
        f(proxy)
        return proxy.value

    return wrapper


def argument(name):

    def decorator(f):
        if not hasattr(f, "arguments"):
            f.arguments = []
        f.arguments.insert(0, name)
        return f

    return decorator


class Result:

    def __init__(self, value=None):
        self.value = value


class Success:

    def __init__(self, **kwargs):
        self.kwargs = kwargs


class Failure:

    def __repr__(self):
        return self.__class__.__name__


class Context:

    def __init__(self, ns):
        self.ns = ns

    def __getattr__(self, name):
        return self.ns[name]


class Proxy:

    def __init__(self, other, ctx):
        self.other = other
        self.ctx = ctx
        self.done = False

    def __getattr__(self, name):
        attr = getattr(self.other.__class__, name, undefined)
        if attr is undefined:
            attr = getattr(self.other, name)
        elif callable(attr):
            attr = MethodWrapper(self, attr)
        return attr


class MethodWrapper:

    def __init__(self, proxy, method):
        self.proxy = proxy
        self.method = method

    def __call__(self):
        if self.proxy.done:
            return self.proxy.value

        result = self.method(self.proxy)
        restype = type(result)
        assert restype in (Result, Success, Failure)

        if restype is Failure:
            value = self.proxy.value = result
            self.proxy.done = True
        elif restype is Result:
            value = self.proxy.value = result.value
            self.proxy.done = True
        else:
            assert not set(self.proxy.ctx.ns) & set(result.kwargs)
            self.proxy.ctx.ns.update(result.kwargs)
            value = self.proxy.value = None

        return value
