# Stories

[![azure-devops-builds](https://img.shields.io/azure-devops/build/proofit404/stories/3?style=flat-square)](https://dev.azure.com/proofit404/stories/_build/latest?definitionId=3&branchName=master)
[![azure-devops-coverage](https://img.shields.io/azure-devops/coverage/proofit404/stories/3?style=flat-square)](https://dev.azure.com/proofit404/stories/_build/latest?definitionId=3&branchName=master)
[![pypi](https://img.shields.io/pypi/v/stories?style=flat-square)](https://pypi.python.org/pypi/stories/)

The business transaction DSL.

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

This code style allow you clearly separate actual business scenario from
implementation details.

## License

Stories library is offered under the two clause BSD license.

<p align="center">&mdash; ⭐️ &mdash;</p>
<p align="center"><i>The stories library is part of the SOLID python family.</i></p>
