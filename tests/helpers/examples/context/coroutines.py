from examples.context import *  # noqa: F401, F403
from stories import Result
from stories import Success


# Mixins.


class PrivateMethod:
    async def one(self, ctx):
        return Result(ctx.__dict__)


class NormalMethod:
    async def one(self, ctx):
        ctx.foo = self.foo
        return Success()


class DeleteMethod:
    async def one(self, ctx):
        del ctx.foo


class CompareMethod:
    async def one(self, ctx):
        if ctx:
            pass  # pragma: no cover


class DirMethod:
    async def one(self, ctx):
        return Result(dir(ctx))


# Parent mixins.


class NormalParentMethod:
    async def before(self, ctx):
        return Success()

    async def after(self, ctx):
        return Success()


class DirParentMethod:
    async def before(self, ctx):
        return Success()

    async def after(self, ctx):
        return Result(dir(ctx))
