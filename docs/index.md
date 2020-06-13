# Stories

[![azure-devops-builds](https://img.shields.io/azure-devops/build/proofit404/stories/3?style=flat-square)](https://dev.azure.com/proofit404/stories/_build/latest?definitionId=3&branchName=master)
[![azure-devops-coverage](https://img.shields.io/azure-devops/coverage/proofit404/stories/3?style=flat-square)](https://dev.azure.com/proofit404/stories/_build/latest?definitionId=3&branchName=master)
[![pypi](https://img.shields.io/pypi/v/stories?style=flat-square)](https://pypi.python.org/pypi/stories/)

The business transaction DSL.

**[Documentation](https://proofit404.github.io/stories/) | [Source Code](https://github.com/proofit404/stories) | [Task Tracker](https://github.com/proofit404/stories/issues)**

`stories` is a business transaction DSL. It provides a simple way to
define a complex business transaction that includes processing over
many steps and by many different objects. It makes error handling a
primary concern by taking a “[Railway Oriented
Programming](http://fsharpforfunandprofit.com/rop/)” approach to
capturing and returning errors from any step in the transaction.

## Pros

- Define a user story in the business transaction DSL.
- Separate state, implementation and specification.
- Clean flow in the source code.
- Separate step implementation.
- Each step knows nothing about a neighbor.
- Easy reuse of code.
- Allows to instrument code easily.
- Explicit data contracts and relations in code.
- Data store independent.
- Catch errors when they occur.
- Not when they propagate to exception.

`stories` is based on the following ideas:

- A business transaction is a series of operations where any can fail
  and stop the processing.
- A business transaction can describe its steps on an abstract level
  without being coupled to any details about how individual operations
  work.
- A business transaction doesn’t have any state.
- Each operation shouldn’t accumulate state, instead it should receive
  an input and return an output without causing any side-effects.
- The only interface of an operation is `ctx`.
- Each operation provides a meaningful piece of functionality and can
  be reused.
- Errors in any operation should be easily caught and handled as part
  of the normal application flow.

## Example

`stories` provide a simple way to define a complex business scenario
that include many processing steps.

```pycon tab="sync"

>>> from stories import story, arguments, Success, Failure, Result
>>> from app.repositories import load_category, load_profile, create_subscription

>>> class Subscribe:
...
...     @story
...     @arguments('category_id', 'profile_id')
...     def buy(I):
...
...         I.find_category
...         I.find_profile
...         I.check_balance
...         I.persist_subscription
...         I.show_subscription
...
...     def find_category(self, ctx):
...
...         ctx.category = load_category(ctx.category_id)
...         return Success()
...
...     def find_profile(self, ctx):
...
...         ctx.profile = load_profile(ctx.profile_id)
...         return Success()
...
...     def check_balance(self, ctx):
...
...         if ctx.category.cost < ctx.profile.balance:
...             return Success()
...         else:
...             return Failure()
...
...     def persist_subscription(self, ctx):
...
...         ctx.subscription = create_subscription(category=ctx.category, profile=ctx.profile)
...         return Success()
...
...     def show_subscription(self, ctx):
...
...         return Result(ctx.subscription)

>>> Subscribe().buy(category_id=1, profile_id=1)
Subscription(primary_key=8)

```

```pycon tab="async"

>>> import asyncio
>>> from stories import story, arguments, Success, Failure, Result
>>> from aioapp.repositories import load_category, load_profile, create_subscription

>>> class Subscribe:
...
...     @story
...     @arguments('category_id', 'profile_id')
...     def buy(I):
...
...         I.find_category
...         I.find_profile
...         I.check_balance
...         I.persist_subscription
...         I.show_subscription
...
...     async def find_category(self, ctx):
...
...         ctx.category = await load_category(ctx.category_id)
...         return Success()
...
...     async def find_profile(self, ctx):
...
...         ctx.profile = await load_profile(ctx.profile_id)
...         return Success()
...
...     async def check_balance(self, ctx):
...
...         if ctx.category.cost < ctx.profile.balance:
...             return Success()
...         else:
...             return Failure()
...
...     async def persist_subscription(self, ctx):
...
...         ctx.subscription = await create_subscription(category=ctx.category, profile=ctx.profile)
...         return Success()
...
...     async def show_subscription(self, ctx):
...
...         return Result(ctx.subscription)

>>> asyncio.run(Subscribe().buy(category_id=1, profile_id=1))
Subscription(primary_key=9)

```

This code style allow you clearly separate actual business scenario from
implementation details.

## Questions

If you have any questions, feel free to create an issue in our [Task Tracker](https://github.com/proofit404/stories/issues). We have the [question label](https://github.com/proofit404/stories/issues?q=is%3Aopen+is%3Aissue+label%3Aquestion) exactly for this purpose.

## License

Stories library is offered under the two clause BSD license.

<p align="center">&mdash; ⭐️ &mdash;</p>
<p align="center"><i>The stories library is part of the SOLID python family.</i></p>
