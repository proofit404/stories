=============
 Composition
=============

Sometimes you want to split your business logic into several parts
inside single story.  Obviously, you want to do so to be able to reuse
this parts in different stories.  Or maybe your goal is grouping
several steps into a sub-story for readability.

There are a several ways to do it.

Class methods
=============

You can write sub-stories in the same class and use them as steps as a
parent story step.

If you want the parent story to provide some context variables, use
``@argument`` decorator on the sub-story definition.

.. code:: python

    class Subscription:

        @story
        @argument("category_id")
        @argument("price_id")
        @argument("user")
        def buy(I):

            I.find_category
            I.find_price
            I.find_promo_code
            I.find_profile
            I.check_balance
            I.persist_payment
            I.persist_subscription
            I.send_subscription_notification
            I.show_category

        @story
        @argument("category")
        @argument("price")
        def find_promo_code(I):

            I.find_token
            I.check_expiration
            I.calculate_discount

You can see final composition in the class result representation:

.. code:: python

    >>> Subscription.buy
    Subscription.buy:
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
    >>> _

Instance attributes
===================

We prefer to define our business logic in a separate components with
lose coupling.  The final thing will be built later using composition.
We use well known technique called `Constructor dependency injection`_
for it.  The key point here: you can add story steps directly to the
instance with attribute assignment.  No matter where this steps come
from, constructor or not.

.. code:: python

    class Subscription:

        @story
        @argument("category_id")
        @argument("price_id")
        @argument("user")
        def buy(I):

            I.find_category
            I.find_price
            I.find_promo_code
            I.find_profile
            I.check_balance
            I.persist_payment
            I.persist_subscription
            I.send_subscription_notification
            I.show_category

        def __init__(self, find_promo_code):

            self.find_promo_code = find_promo_code

    class PromoCode:

        @story
        @argument("category")
        @argument("price")
        def find(I):

            I.find_token
            I.check_expiration
            I.calculate_discount

At this moment, story definition does not know what
``find_promo_code`` step should be.

.. code:: python

    >>> Subscription.buy
    Subscription.buy:
      find_category
      find_price
      find_promo_code ??
      find_profile
      check_balance
      persist_payment
      persist_subscription
      send_subscription_notification
      show_category
    >>> _

And when we create instance of the class we will specify this
explicitly.  Representation of the instance attribute will show us
complete story.

.. code:: python

    >>> Subscription(PromoCode().find).buy
    Subscription.buy:
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
    >>> _

Delegate implementation
=======================

TODO: Sub-story with implementation DI.

.. _constructor dependency injection: https://en.wikipedia.org/wiki/Dependency_injection#Constructor_injection
