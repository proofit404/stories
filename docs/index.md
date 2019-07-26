![logo](https://raw.githubusercontent.com/dry-python/brand/master/logo/stories.png)

[![azure-pipeline](https://dev.azure.com/dry-python/stories/_apis/build/status/dry-python.stories?branchName=master)](https://dev.azure.com/dry-python/stories/_build/latest?definitionId=3&branchName=master)
[![codecov](https://codecov.io/gh/dry-python/stories/branch/master/graph/badge.svg)](https://codecov.io/gh/dry-python/stories)
[![docs](https://readthedocs.org/projects/stories/badge/?version=latest)](https://stories.readthedocs.io/en/latest/?badge=latest)
[![gitter](https://badges.gitter.im/dry-python/stories.svg)](https://gitter.im/dry-python/stories)
[![pypi](https://img.shields.io/pypi/v/stories.svg)](https://pypi.python.org/pypi/stories/)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

-----

# The business transaction DSL

`stories` is a business transaction DSL. It provides a simple way to
define a complex business transaction that includes processing over
many steps and by many different objects. It makes error handling a
primary concern by taking a “[Railway Oriented
Programming](http://fsharpforfunandprofit.com/rop/)” approach to
capturing and returning errors from any step in the transaction.

`stories` is based on the following ideas:

* A business transaction is a series of operations where any can fail
  and stop the processing.
* A business transaction can describe its steps on an abstract level
  without being coupled to any details about how individual operations
  work.
* A business transaction doesn’t have any state.
* Each operation shouldn’t accumulate state, instead it should receive
  an input and return an output without causing any side-effects.
* The only interface of an operation is `ctx`.
* Each operation provides a meaningful piece of functionality and can
  be reused.
* Errors in any operation should be easily caught and handled as part
  of the normal application flow.

# Example

`stories` provide a simple way to define a complex business scenario
that include many processing steps.

```pycon

>>> from stories import story, arguments, Success, Failure, Result
>>> from app.models import Category, Profile, Subscription

>>> class Subscribe:
...
...     @story
...     @arguments('category_id', 'user_id')
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
...         category = Category.objects.get(id=ctx.category_id)
...         return Success(category=category)
...
...     def find_profile(self, ctx):
...
...         profile = Profile.objects.get(user_id=ctx.user_id)
...         return Success(profile=profile)
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
...         subscription = Subscription(ctx.category, ctx.profile)
...         subscription.save()
...         return Success(subscription=subscription)
...
...     def show_subscription(self, ctx):
...
...         return Result(ctx.subscription)

```

```pycon

>>> Subscribe().buy(category_id=1, user_id=1)
<Subscription object (1)>

```

This code style allow you clearly separate actual business scenario from
implementation details.

!!! note
    `stories` library was heavily inspired by
    [dry-transaction](http://dry-rb.org/gems/dry-transaction/) ruby gem.
