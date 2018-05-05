"""
stories
-------

This module implements Business Transaction DSL.

:copyright: (c) 2018 by Artem Malyshev.
:license: BSD, see LICENSE for more details.
"""


__all__ = ["story", "argument", "Result", "Success", "Failure", "Skip"]


import sys


class story(object):

    def __init__(self, f):
        self.f = f

    def __get__(self, obj, cls):
        return StoryWrapper(obj, cls, self.f)


def argument(name):

    def decorator(f):
        if not hasattr(f, "arguments"):
            f.arguments = []
        f.arguments.insert(0, name)
        return f

    return decorator


class Result(object):

    def __init__(self, value=None):
        self.value = value

    def __repr__(self):
        return self.__class__.__name__ + "(" + repr(self.value) + ")"


class Success(object):

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __repr__(self):
        return self.__class__.__name__ + namespace_representation(self.kwargs)


class Failure(object):

    def __repr__(self):
        return self.__class__.__name__ + "()"


class Skip(object):

    def __repr__(self):
        return self.__class__.__name__ + "()"


undefined = object()


class StoryWrapper(object):

    def __init__(self, obj, cls, f):
        self.obj = obj
        self.cls = cls
        self.f = f

    def __call__(self, *args, **kwargs):
        return tell_the_story(self.obj, self.f, args, kwargs)

    def run(self, *args, **kwargs):
        return run_the_story(self.obj, self.f, args, kwargs)

    def __repr__(self):
        return story_representation(self)


def tell_the_story(obj, f, args, kwargs):

    ctx = Context(validate_arguments(f, args, kwargs))
    the_story = []
    f(Collector(obj, the_story, f))
    skipped = undefined

    for self, method, of in the_story:

        if skipped is not undefined:
            if method is end_of_story and skipped is of:
                skipped = undefined
            continue

        result = method(make_proxy(self, ctx))
        if result is undefined:
            continue

        restype = type(result)
        assert restype in (Result, Success, Failure, Skip)

        if restype is Failure:
            return result

        if restype is Result:
            return result.value

        if restype is Skip:
            skipped = of
            continue

        assert not set(ctx.ns) & set(result.kwargs)
        ctx.ns.update(result.kwargs)


def run_the_story(obj, f, args, kwargs):

    ctx = Context(validate_arguments(f, args, kwargs))
    the_story = []
    f(Collector(obj, the_story, f))
    skipped = undefined

    for self, method, of in the_story:

        if skipped is not undefined:
            if method is end_of_story and skipped is of:
                skipped = undefined
            continue

        result = method(make_proxy(self, ctx))
        if result is undefined:
            continue

        restype = type(result)
        assert restype in (Result, Success, Failure, Skip)

        if restype is Failure:
            return Summary(
                is_success=False,
                is_failure=True,
                returned=None,
                failed_method=method.__name__,
            )

        if restype is Result:
            return Summary(
                is_success=True,
                is_failure=False,
                returned=result.value,
                failed_method=None,
            )

        if restype is Skip:
            skipped = of
            continue

        assert not set(ctx.ns) & set(result.kwargs)
        ctx.ns.update(result.kwargs)

    return Summary(is_success=True, is_failure=False, returned=None, failed_method=None)


def validate_arguments(f, args, kwargs):

    assert not (args and kwargs)
    arguments = getattr(f, "arguments", [])

    if args:
        assert len(arguments) == len(args)
        return {k: v for k, v in zip(arguments, args)}

    assert set(arguments) == set(kwargs)
    return kwargs


class Context(object):

    def __init__(self, ns):
        self.ns = ns

    def __getattr__(self, name):
        return self.ns[name]

    def __repr__(self):
        return self.__class__.__name__ + namespace_representation(self.ns)


class Collector(object):

    def __init__(self, obj, method_calls, of):
        self.obj = obj
        self.method_calls = method_calls
        self.of = of

    def __getattr__(self, name):

        attribute = getattr(self.obj.__class__, name, undefined)

        if attribute is not undefined:
            if is_story(attribute):
                collect_substory(attribute.f, self.obj, self.method_calls)
                return lambda: None

            self.method_calls.append((self.obj, attribute, self.of))
            return lambda: None

        attribute = getattr(self.obj, name)
        assert is_story(attribute)
        collect_substory(attribute.f, attribute.obj, self.method_calls)
        return lambda: None


PY3 = sys.version_info[0] >= 3


if PY3:

    def make_proxy(obj, ctx):
        return Proxy(obj, ctx)


else:

    def make_proxy(obj, ctx):

        class ObjectProxy(Proxy, obj.__class__):
            pass

        return ObjectProxy(obj, ctx)


class Proxy(object):

    def __init__(self, obj, ctx):
        self.obj = obj
        self.ctx = ctx

    def __getattr__(self, name):
        return getattr(self.obj, name)


class Summary(object):

    def __init__(self, is_success, is_failure, returned, failed_method):
        self.is_success = is_success
        self.is_failure = is_failure
        self.returned = returned
        self.failed_method = failed_method

    def failed_on(self, method_name):
        return self.is_failure and method_name == self.failed_method

    @property
    def value(self):
        assert self.is_success
        return self.returned


def is_story(attribute):
    return callable(attribute) and type(attribute) is StoryWrapper


def collect_substory(f, obj, method_calls):

    arguments = getattr(f, "arguments", [])

    def validate_substory_arguments(self):
        assert set(arguments) <= set(self.ctx.ns)
        return undefined

    method_calls.append((obj, validate_substory_arguments, f))
    f(Collector(obj, method_calls, f))
    method_calls.append((obj, end_of_story, f))


def end_of_story(self):
    return undefined


def namespace_representation(ns):
    return "(" + ", ".join([k + "=" + repr(v) for k, v in ns.items()]) + ")"


def story_representation(wrapper):

    lines = [wrapper.cls.__name__ + "." + wrapper.f.__name__]
    represent = Represent(wrapper, lines, 1)
    wrapper.f(represent)
    if not represent.touched:
        lines.append("  <empty>")
    return "\n".join(lines)


class Represent(object):

    def __init__(self, wrapper, lines, level):
        self.wrapper = wrapper
        self.lines = lines
        self.level = level
        self.touched = False

    def __getattr__(self, name):
        self.touched = True
        attribute = getattr(self.wrapper.obj.__class__, name, undefined)
        if attribute is not undefined and is_story(attribute):
            self.lines.append("  " * self.level + name)
            represent = Represent(self.wrapper, self.lines, self.level + 1)
            attribute.f(represent)
            if not represent.touched:
                self.lines.append("  " * (self.level + 1) + "<empty>")
            return lambda: None

        attribute = getattr(self.wrapper.obj, name, undefined)
        if attribute is not undefined and is_story(attribute):
            self.lines.append(
                "  "
                * self.level
                + name
                + " ("
                + attribute.cls.__name__
                + "."
                + attribute.f.__name__
                + ")"
            )
            represent = Represent(attribute, self.lines, self.level + 1)
            attribute.f(represent)
            if not represent.touched:
                self.lines.append("  " * (self.level + 1) + "<empty>")
            return lambda: None

        self.lines.append("  " * self.level + name)
        return lambda: None
