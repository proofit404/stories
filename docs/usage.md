# Usage

There are several methods to use business object defined with the
`@story` decorator.

## Call

The most simple variant to execute story is to call it as a regular
method.

### Result

```pycon tab="sync"

>>> from app.services import Subscription

>>> Subscription().buy(category_id=1, price_id=1, profile_id=1)
Category(primary_key=1, name='Books', cost=7)

```

```pycon tab="async"

>>> import asyncio
>>> from aioapp.services import Subscription

>>> asyncio.run(Subscription().buy(category_id=1, price_id=1, profile_id=1))
Category(primary_key=1, name='Books', cost=7)

```

The story was executed successfully. It returns an object we put into
`Result` marker.

### Failure

```pycon tab="sync"

>>> from app.services import Subscription

>>> Subscription().buy(category_id=2, price_id=2, profile_id=1)
Traceback (most recent call last):
  ...
_stories.exceptions.FailureError

```

```pycon tab="async"

>>> from aioapp.services import Subscription

>>> asyncio.run(Subscription().buy(category_id=2, price_id=2, profile_id=1))
Traceback (most recent call last):
  ...
_stories.exceptions.FailureError

```

Story failed. The user does not have enough money to complete this
purchase. `Failure` marker throws an exception when `call` method was
used.

## Run

A more powerful way to inspect the result of the story is to use the
`run` method instead.

The `run` method always returns an object. This object contains a
summary of the business object execution.

### Result

```pycon tab="sync"

>>> from app.services import ShowCategory

>>> result = ShowCategory().show.run(category_id=1, profile_id=1)

>>> result.is_success
True

>>> result.value
Category(primary_key=1, name='Books', cost=7)

```

```pycon tab="async"

>>> import asyncio
>>> from aioapp.services import ShowCategory

>>> result = asyncio.run(ShowCategory().show.run(category_id=1, profile_id=1))

>>> result.is_success
True

>>> result.value
Category(primary_key=1, name='Books', cost=7)

```

If the story was executed successfully, its actual result will be
available in the `value` attribute.

### Failure

```pycon tab="sync"

>>> from app.services import ShowCategory

>>> result = ShowCategory().show.run(category_id=2, profile_id=1)

>>> result.is_failure
True

>>> result.failed_on("check_expiration")
True

>>> result.failed_because(ShowCategory().show.failures.forbidden)
True

>>> result.ctx
ShowCategory.show
  find_subscription
  check_expiration (failed: <Errors.forbidden: 1>)
<BLANKLINE>
Context:
  category_id: 2                             # Story argument
  profile_id: 1                              # Story argument
  subscription: Subscription(primary_key=7)  # Set by ShowCategory.find_subscription

>>> result.ctx.subscription.is_expired()
True

>>> result.ctx.subscription.created
datetime.date(2019, 1, 1)

```

```pycon tab="async"

>>> from aioapp.services import ShowCategory

>>> result = asyncio.run(ShowCategory().show.run(category_id=2, profile_id=1))

>>> result.is_failure
True

>>> result.failed_on("check_expiration")
True

>>> result.failed_because(ShowCategory().show.failures.forbidden)
True

>>> result.ctx
ShowCategory.show
  find_subscription
  check_expiration (failed: <Errors.forbidden: 1>)
<BLANKLINE>
Context:
  category_id: 2                             # Story argument
  profile_id: 1                              # Story argument
  subscription: Subscription(primary_key=7)  # Set by ShowCategory.find_subscription

>>> result.ctx.subscription.is_expired()
True

>>> result.ctx.subscription.created
datetime.date(2019, 1, 1)

```

`run` does not raise an error. Even if the story returns `Failure`
marker.

Instead, you can use methods like `failed_on` and `failed_because` to
look for failed story method and exact reason. The argument used in
the `failed_because` method will be described in more details in the
[failure protocol](failure_protocol.md) chapter.

The context of the failed story is also available in the result object.

<p align="center">&mdash; ⭐️ &mdash;</p>
<p align="center"><i>The stories library is part of the SOLID python family.</i></p>
