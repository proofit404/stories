![logo](https://raw.githubusercontent.com/dry-python/brand/master/logo/stories.png)

[![azure-pipeline](https://dev.azure.com/dry-python/stories/_apis/build/status/dry-python.stories?branchName=master)](https://dev.azure.com/dry-python/stories/_build/latest?definitionId=3&branchName=master)
[![codecov](https://codecov.io/gh/dry-python/stories/branch/master/graph/badge.svg)](https://codecov.io/gh/dry-python/stories)
[![docs](https://readthedocs.org/projects/stories/badge/?version=latest)](https://stories.readthedocs.io/en/latest/?badge=latest)
[![gitter](https://badges.gitter.im/dry-python/stories.svg)](https://gitter.im/dry-python/stories)
[![pypi](https://img.shields.io/pypi/v/stories.svg)](https://pypi.python.org/pypi/stories/)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

---

# The business transaction DSL

- [Source Code](https://github.com/dry-python/stories)
- [Issue Tracker](https://github.com/dry-python/stories/issues)
- [Documentation](https://stories.readthedocs.io/en/latest/)
- [Discussion](https://gitter.im/dry-python/stories)

## Installation

All released versions are hosted on the Python Package Index. You can
install this package with following command.

```bash
pip install stories
```

## Usage

`stories` provide a simple way to define a complex business scenario
that include many processing steps.

```pycon

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
...         category = Category.objects.get(pk=ctx.category_id)
...         return Success(category=category)
...
...     def find_profile(self, ctx):
...
...         profile = Profile.objects.get(pk=ctx.profile_id)
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
...         subscription = Subscription(category=ctx.category, profile=ctx.profile)
...         subscription.save()
...         return Success(subscription=subscription)
...
...     def show_subscription(self, ctx):
...
...         return Result(ctx.subscription)

```

```pycon

>>> Subscribe().buy(category_id=1, profile_id=1)
<Subscription: Subscription object (8)>

```

This code style allow you clearly separate actual business scenario from
implementation details.

## License

Stories library is offered under the two clause BSD license.
