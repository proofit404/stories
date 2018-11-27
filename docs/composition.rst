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

TODO: Sub-story with DI.

TODO: Sub-story with DI class representation.

TODO: Sub-story with DI instance representation.

TODO: Sub-story with implementation DI.

TODO: Refer to this paragraph in the Debugging -> Code "You can read more on this topic here."
