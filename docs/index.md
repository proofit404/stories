![logo](https://raw.githubusercontent.com/dry-python/brand/master/logo/stories.png)

[![azure-devops-builds](https://img.shields.io/azure-devops/build/dry-python/stories/3?style=flat-square)](https://dev.azure.com/dry-python/stories/_build/latest?definitionId=3&branchName=master)
[![azure-devops-coverage](https://img.shields.io/azure-devops/coverage/dry-python/stories/3?style=flat-square)](https://dev.azure.com/dry-python/stories/_build/latest?definitionId=3&branchName=master)
[![readthedocs](https://img.shields.io/readthedocs/stories?style=flat-square)](https://stories.readthedocs.io/en/latest/?badge=latest)
[![gitter](https://img.shields.io/gitter/room/dry-python/stories?style=flat-square)](https://gitter.im/dry-python/stories)
[![pypi](https://img.shields.io/pypi/v/stories?style=flat-square)](https://pypi.python.org/pypi/stories/)

---

# The business transaction DSL

`stories` is a business transaction DSL. It provides a simple way to
define a complex business transaction that includes processing over
many steps and by many different objects. It makes error handling a
primary concern by taking a “[Railway Oriented
Programming](http://fsharpforfunandprofit.com/rop/)” approach to
capturing and returning errors from any step in the transaction.

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

# Example

`stories` provide a simple way to define a complex business scenario
that include many processing steps.

```pycon tab="sync"

>>> from stories import story, arguments, Success, Failure, Result
>>> from django_project.models import Category, Profile, Subscription

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
...         ctx.category = Category.objects.get(pk=ctx.category_id)
...         return Success()
...
...     def find_profile(self, ctx):
...
...         ctx.profile = Profile.objects.get(pk=ctx.profile_id)
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
...         ctx.subscription = Subscription(category=ctx.category, profile=ctx.profile)
...         ctx.subscription.save()
...         return Success()
...
...     def show_subscription(self, ctx):
...
...         return Result(ctx.subscription)

>>> Subscribe().buy(category_id=1, profile_id=2)
<Subscription: Subscription object (9)>

```

```pycon tab="async"

>>> from stories import story, arguments, Success, Failure, Result
>>> from django_project.models import Category, Profile, Subscription

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
...         ctx.category = await Category.objects.get(pk=ctx.category_id)
...         return Success()
...
...     async def find_profile(self, ctx):
...
...         ctx.profile = await Profile.objects.get(pk=ctx.profile_id)
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
...         ctx.subscription = Subscription(
...             category=ctx.category, profile=ctx.profile
...         )
...         await ctx.subscription.save()
...         return Success()
...
...     async def show_subscription(self, ctx):
...
...         return Result(ctx.subscription)

>>> await Subscribe().buy(category_id=1, profile_id=2)  # doctest: +SKIP
<Subscription: Subscription object (9)>

```

This code style allow you clearly separate actual business scenario from
implementation details.

!!! note

    `stories` library was heavily inspired by
    [dry-transaction](http://dry-rb.org/gems/dry-transaction/) ruby gem.

<p align="center">&mdash; ⭐️ &mdash;</p>
<p align="center"><i>Drylabs maintains dry-python and helps those who want to use it inside their organizations.</i></p>
<p align="center"><i>Read more at <a href="https://drylabs.io">drylabs.io</a></i></p>
