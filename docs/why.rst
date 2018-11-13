=====
 Why
=====

Good code is easy to understand and change.  We build ``stories`` to
make your project both easier to understand and to change.

Lets consider common situations during development.

Micro framework
===============

Macro framework
===============

Business logic
==============

The main problem with both approaches - it is completely unclear what
the application actually does?  What problems it is trying to solve?

Most frameworks are busy with forms, serializers, transport layers,
field mappings.  And all these implementation details are not the
right abstractions for decision making.

DSL
===

Wouldn't it be nice if we can just read business logic as it was
intended?

.. code:: python

    from stories import story, argument

    class Subscription:
        @story
        @argument("category_id")
        @argument("price_id")
        def buy(I):
            I.find_category
            I.find_price
            I.find_profile
            I.check_balance
            I.persist_payment
            I.persist_subscription
            I.send_subscription_notification

Wouldn't it be nice to have a clear understanding of the actual sate
and execution path?

.. code:: python

    >>> ctx
    Subscription.buy:
      find_category
      check_price
      check_purchase (PromoCode.validate)
        find_code (skipped)
      check_balance
        find_profile

    Context:
      category_id = 1318  # Story argument
      user = <User: 3292> # Story argument
      category = <Category: 1318>
        # Set by Subscription.find_category
    >>> _

Wouldn't it be nice to know which line of the test execute what
business scenarios?

.. image:: /static/pytest.png

Wouldn't it be nice to see the same about your view in the debug
toolbar?

.. image:: /static/debug-toolbar.png

Wouldn't it be nice to have the same detailed picture for production
failures?

.. image:: /static/sentry.png

Interesting, isn't it?  Check out Usage guide to learn more.
