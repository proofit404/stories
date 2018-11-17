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

Micro frameworks doesn't offer too much structure to your project.
The main goal is flexibility.  And you're mostly on your own when it
comes to organize your code.

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

We does not have any information about this strange comparison
expression.

Let's consider we should process this data in a different way to
complete our current task.

We decide to change this expression.

Of course we test all possible scenarios we can imagine.

But after some time this error would happen in the production:

.. code:: python

    Traceback (most recent call last):
      File "views.py", line 1027, in buy_subscription
    ZeroDivisionError: division by zero

Turns out there were a lot more variants of incoming data than we can
imagine.  So our change failed in several business scenarios.

This happens because our code wasn't written to help us understand it.

Macro framework
===============

On the other side there are a lot of technologies with strong opinions
how to structure programs written with their help.

This approach also has its own cost.

1. You need method flowchart to understand data flow in your system.
2. Zig-zag traceback problem.  It's hard to figure out the actual
   execution path because your code always mixed with code of the
   framework.
3. Framework internals leak in to your code base.

Let's consider this view:

.. code:: python

    class SubscriptionViewSet(viewsets.ModelViewSet):
        queryset = Subscription.objects.all()
        serializer_class = SubscriptionSerializer
        permission_classes = (CanSubscribe,)
        filter_class = SubscriptionFilter

The only thing we can clue about - it is somehow related to the
subscription to our service.

But it does not tell us:

1. What exactly does this class do?
2. How to use it?

We need to keep framework documentation close to the sources to figure
this out.

.. image:: /static/method-flowchart.png

After few hours of digging we will figure out there are about 17
different ways to interact with this view.

When we goes to the ``SubscriptionSerializer`` class, we expect to see
there a mapping of fields from database model to the json object.

And we actually do.  But in addition we see this method:

.. code:: python

    def recreate_nested_writable_fields(self, instance):
        for field, values in self.writable_fields_to_recreate():
            related_manager = getattr(instance, field)
            related_manager.all().delete()
            for data in values:
                obj = related_manager.model.objects.create(
                    to=instance, **data)
                related_manager.add(obj)

Once again we have no idea...

1. What was the actual reason to put this method there?
2. Which one of the 17 ways to interact with the view it affects?
3. What framework state it expect to work with?

It will take few hours more to answer this questions.

Conclusion
==========

In both projects built with ``micro`` and ``macro`` frameworks we end
up with actually the **same** situation:

1. Our code is fragile.  We afraid to change it.
2. It is hard to reason about.
3. It is time-consuming to work with it.

But there is a solution for it!

Business logic
==============

The main problem with both approaches - it is completely unclear what
the application actually do.  What problems it is trying to solve?

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

Wouldn't it be nice to have a clear understandable state?

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

Wouldn't it be nice to know which business scenario was executed by
every line in the tests?

.. image:: /static/pytest.png

Wouldn't it be nice to see the same details in the debug toolbar?

.. image:: /static/debug-toolbar.png

Wouldn't it be nice to it when production fails?

.. image:: /static/sentry.png

Interesting, isn't it?  Check out Usage guide to learn more.
