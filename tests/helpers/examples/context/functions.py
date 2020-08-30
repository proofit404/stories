from examples.context import *  # noqa: F401, F403
from stories import Result
from stories import Success


# Mixins.


class PrivateMethod:
    def one(self, ctx):
        return Result(ctx.__dict__)


class NormalMethod:
    def one(self, ctx):
        ctx.foo = self.foo
        return Success()


class DeleteMethod:
    def one(self, ctx):
        del ctx.foo


class CompareMethod:
    def one(self, ctx):
        if ctx:
            pass  # pragma: no cover


class DirMethod:
    def one(self, ctx):
        return Result(dir(ctx))


# Parent mixins.


class NormalParentMethod:
    def before(self, ctx):
        return Success()

    def after(self, ctx):
        return Success()


class DirParentMethod:
    def before(self, ctx):
        return Success()

    def after(self, ctx):
        return Result(dir(ctx))
