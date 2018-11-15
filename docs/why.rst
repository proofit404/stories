=====
 Why
=====

Good code is easy to understand and change.  We build ``stories`` with
this constrains in mind.

``stories`` force you to write structured, understandable code with
right separation of concerns and responsibilities.

Lets consider common troubles you meat in development.

Micro framework
===============

Micro frameworks doesn't offer too much structure on your project.
The main goal is flexibility.

Most of the times you will end up with two problems:

1. Long view functions.
2. Lots of ``if`` statements inside this functions.

There is a lot of complexity in it.

Let's consider following view function.

.. code:: python

     85 @app.route('/subscriptions/')
     86 def buy_subscription(page):
    ...
    121     if props[-1].endswith('$'):
    122 ->      props[-1] = props[-1][:-1]
    123

We does not have any information about this strange condition.  To
complete our current task we should process this data in a different
way.

We decide to change this condition.  Of course we test all possible
scenarios we can imagine.

But after some times we will found this in the production:

.. code:: python

    Traceback (most recent call last):
      File "views.py", line 1027, in buy_subscription
    ZeroDivisionError: division by zero

Turns out there were a lot more variants of income data we can
imagine.  So our change failed in one business scenario.

This happens because this code wasn't written to help us understand
the business case of it.

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
