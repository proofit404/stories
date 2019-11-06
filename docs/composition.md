# Composition

Sometimes you want to split your business logic into several parts
inside a single story. Obviously, you want to do so to be able to reuse
this parts in different stories. Or maybe your goal is grouping several
steps into a sub-story for readability.

There are several ways to do it.

!!! note

    [Failure protocol](failure_protocol.md) of the story composition is
    [composition itself](failure_protocol.md#composition). It will use all
    reasons for all protocols of all stories used in the composition.

## Class methods

You can write sub-stories in the same class and use them as steps as a
parent story step.

If you want the parent story to provide some context variables, use
`@arguments` decorator on the sub-story definition.

!!! note

    We advise all users to define step definition methods in the same
    class with stories which use them.  We use inheritance from
    `MethodDefinitions` base class for brevity.

```pycon

>>> from stories import story, arguments, Success, Failure
>>> from django_project.services import MethodDefinitions

>>> class Subscription(MethodDefinitions):
...
...     @story
...     @arguments("category_id", "price_id", "profile_id")
...     def buy(I):
...
...         I.find_category
...         I.find_price
...         I.find_promo_code
...         I.find_profile
...         I.check_balance
...         I.persist_payment
...         I.persist_subscription
...         I.send_subscription_notification
...         I.show_category
...
...     @story
...     @arguments("category", "price")
...     def find_promo_code(I):
...
...         I.find_token
...         I.check_expiration
...         I.calculate_discount

```

You can see final composition in the class result representation:

```pycon

>>> Subscription.buy
Subscription.buy
  find_category
  find_price
  find_promo_code
    find_token
    check_expiration
    calculate_discount
  find_profile
  check_balance
  persist_payment
  persist_subscription
  send_subscription_notification
  show_category

```

## Instance attributes

We prefer to define our business logic in separate components with loose
coupling. The final thing will be built later using composition. We use
a well-known technique called [Constructor dependency
injection](https://en.wikipedia.org/wiki/Dependency_injection#Constructor_injection)
for it. The key point here: you can add story steps directly to the
instance with attribute assignment. No matter where these steps come
from, constructor or not.

```pycon

>>> class Subscription(MethodDefinitions):
...
...     @story
...     @arguments("category_id", "price_id", "profile_id")
...     def buy(I):
...
...         I.find_category
...         I.find_price
...         I.find_promo_code
...         I.find_profile
...         I.check_balance
...         I.persist_payment
...         I.persist_subscription
...         I.send_subscription_notification
...         I.show_category
...
...     def __init__(self, find_promo_code):
...
...         self.find_promo_code = find_promo_code

>>> class PromoCode(MethodDefinitions):
...
...     @story
...     @arguments("category", "price")
...     def find(I):
...
...         I.find_token
...         I.check_expiration
...         I.calculate_discount

```

At this moment, story definition does not know what `find_promo_code`
step should be.

```pycon

>>> Subscription.buy
Subscription.buy
  find_category
  find_price
  find_promo_code ??
  find_profile
  check_balance
  persist_payment
  persist_subscription
  send_subscription_notification
  show_category

```

And when we create an instance of the class we will specify this
explicitly. Representation of the instance attribute will show us the
complete story.

```pycon

>>> Subscription(PromoCode().find).buy
Subscription.buy
  find_category
  find_price
  find_promo_code (PromoCode.find)
    find_token
    check_expiration
    calculate_discount
  find_profile
  check_balance
  persist_payment
  persist_subscription
  send_subscription_notification
  show_category

```

## Delegate implementation

We go even further in this approach. We compose not only stories, but
the actual things we call in our steps come from outside.

> We never call methods of the `Django` model or `requests` package
> directly!

We use simple rules to write our steps.

1. The only thing you can access inside story step is an instance
   method.
2. The return value of this call goes to the context with `Success`
   marker.
3. Decisions are made by comparison context variables to each other or
   using methods of the context variable in the **next** story step.

Here are some examples:

```pycon

>>> class Subscription:
...
...     @story
...     @arguments("profile_id", "price_id")
...     def buy(I):
...
...         I.find_profile
...         I.find_price
...         I.check_balance
...
...     def find_profile(self, ctx):
...
...         profile = self.load_profile(ctx.profile_id)
...         return Success(profile=profile)
...
...     def find_price(self, ctx):
...
...         price = self.load_price(ctx.price_id)
...         return Success(price=price)
...
...     def check_balance(self, ctx):
...
...         if ctx.profile.has_enough_balance(ctx.price):
...             return Success()
...         else:
...             return Failure()
...
...     def __init__(self, load_profile, load_price):
...
...         self.load_profile = load_profile
...         self.load_price = load_price

```

This way you decouple your business logic from relation mapper models or
networking library! There is no more vendor lock on a certain framework
or database! Welcome to the good architecture utopia.

```pycon

>>> from django_project.models import Profile, Price

>>> def load_profile(profile_id):
...     return Profile.objects.get(pk=profile_id)
...

>>> def load_price(price_id):
...     return Price.objects.get(pk=price_id)
...

>>> Subscription(load_profile, load_price).buy(profile_id=1, price_id=7)

```

You can group delegates into a single object to avoid complex
constructors and names duplication.

```pycon

>>> def find_price(self, ctx):
...     price = self.impl.find_price(ctx.price_id)
...     return Success(price=price)

>>> def __init__(self, impl):
...     self.impl = impl

```

If you follow our mantra "decouple everything", you definitely should
check the following libraries:

- [dependencies](https://dependencies.readthedocs.io/)
- [attrs](https://www.attrs.org/)
- [dataclasses](https://docs.python.org/3/library/dataclasses.html)
