============
 Definition
============

Technically speaking, a story is a method of the class which calls
other methods of this class in special order.

The body of the story isn't executed directly.  It's used as a spec of
what should happen.  The main purpose of it is to describe the intent.

Basics
======

This is a real-world example of the story definition used in our
`tutorials`_.  As you can see, it is a business process of the
subscription to our service.

.. code:: python

    from stories import Failure, Result, Success, arguments, story

    class Subscription:
        """Buy subscription for certain category."""

        @story
        @arguments("category_id", "price_id", "user_id")
        def buy(I):

            I.find_category
            I.find_price
            I.find_profile
            I.check_balance
            I.persist_payment
            I.persist_subscription
            I.send_subscription_notification
            I.show_category

        def find_category(self, ctx):

            category = load_category(ctx.category_id)
            return Success(category=category)

        def find_price(self, ctx):

            price = load_price(ctx.price_id)
            return Success(price=price)

        def find_profile(self, ctx):

            profile = load_profile(ctx.user_id)
            return Success(profile=profile)

        def check_balance(self, ctx):

            if ctx.profile.balance > ctx.price.cost:
                return Success()
            else:
                return Failure()

        def persist_payment(self, ctx):

            decrease_balance(ctx.profile, ctx.price.cost)
            save_profile(ctx.profile)
            return Success()

        def persist_subscription(self, ctx):

            expires = calculate_period(ctx.price.period)
            subscription = create_subscription(
                ctx.profile, ctx.category, expires
            )
            return Success(subscription=subscription)

        def send_subscription_notification(self, ctx):

            notification = send_notification(
                "subscription", ctx.profile, ctx.category.name
            )
            return Success(notification=notification)

        def show_category(self, ctx):

            return Result(ctx.category)

Explanation
-----------

There are a few terms you should be familiar with:

1. ``@story`` decorated method represents the spec of the business
   process.  It's executed only once at the class definition moment.
   This class attribute became a smart business object.
2. ``@arguments`` decorator describes input data similar to function
   arguments.
3. ``I`` object is used to build the execution spec out of its
   attributes.  You can use any **human-readable** names.
4. Methods defined in the class are story steps.  They will be called
   by the smart business object defined with the ``@story`` decorator.
   Usually, they just delegate responsibility to the call of other
   function with proper variables from the context.
5. ``self`` in step methods is the real instance of the
   ``Subscription`` class.  You own this class.  It's up to you how to
   write it.  The smart business object will use its instance to
   resolve its steps.
6. ``ctx`` is a scope of variables available to step methods.  Context
   is initiated from input data passed to the business object.  It can
   be extended by previously executed step methods with keyword
   arguments to the ``Success()`` marker.
7. ``Success``, ``Failure`` and ``Result`` are markers returned by
   step methods to change business process execution path.

Failure protocols
=================

To make failure handling a more manageable process we can define a
`failure protocol`_.

.. code:: python

    from enum import Enum, auto
    from stories import Failure, Result, Success, arguments, story

    class ShowCategory:
        """Show category entries."""

        @story
        @arguments("category_id", "user_id")
        def show(I):

            I.find_subscription
            I.check_expiration
            I.find_category
            I.show_category

        def find_subscription(self, ctx):

            subscription = load_subscription(ctx.category_id, ctx.user_id)
            if subscription:
                return Success(subscription=subscription)
            else:
                return Failure(Errors.forbidden)

        def check_expiration(self, ctx):

            if ctx.subscription.is_expired():
                return Failure(Errors.forbidden)
            else:
                return Success()

        def find_category(self, ctx):

            category = load_category(ctx.category_id)
            if category:
                return Success(category=category)
            else:
                return Failure(Errors.not_found)

        def show_category(self, ctx):

            return Result(ctx.category)

    @ShowCategory.show.failures
    class Errors(Enum):

        forbidden = auto()
        not_found = auto()

Explanation
-----------

1. ``Failure`` marker takes optional ``reason`` argument.  It can be
   used to show proper error code to the user.
2. Failure proctor should be defined after the story to allow passing
   ``reason`` in the ``Failure`` marker.

.. _tutorials: https://github.com/dry-python/tutorials
.. _failure protocol: failure_protocol.html
