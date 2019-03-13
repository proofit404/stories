=====
 Why
=====

Good code is easy to understand and change.  We build ``stories`` with
this constrains in mind.

``stories`` force you to write structured, understandable code with
right separation of concerns and responsibilities.

Let's consider common troubles you meet in development.

Micro framework
===============

Micro frameworks don't offer too much structure to your project.  The
main goal is flexibility.  And you're mostly on your own when it comes
to organizing your code.

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

We do not have any information about this strange comparison
expression.

Let's consider we should process this data in a different way to
complete our current task.

We decide to change this expression.

Of course, we test all possible scenarios we can imagine.

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

On the other side, there are a lot of technologies with strong
opinions on how to structure programs written with their help.

This approach also has its own cost.

1. You need method flowchart to understand data flow in your system.
2. Zig-zag traceback problem.  It's hard to figure out the actual
   execution path because your code always mixed with the code of the
   framework.
3. Framework internals leak into your code base.

Let's consider this view:

.. code:: python

    class SubscriptionViewSet(viewsets.ModelViewSet):
        queryset = Subscription.objects.all()
        serializer_class = SubscriptionSerializer
        permission_classes = (CanSubscribe,)
        filter_class = SubscriptionFilter

The only thing we have clue about - it is somehow related to the
subscription to our service.

But it does not tell us:

1. What exactly does this class do?
2. How to use it?

We need to keep framework documentation close to the sources to figure
this out.

.. image:: /static/method-flowchart.png

After a few hours of digging, we will figure out there are about 17
different ways to interact with this view.

When we go to the ``SubscriptionSerializer`` class, we expect to see
there a mapping of fields from the database model to the JSON object.

And we actually do.

.. code:: python

    class SubscriptionSerializer(Serializer):
        category_id = IntegerField()
        price_id = IntegerField()

But in addition we see this method:

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
2. Which one of the 17 ways to interact with the view does it affect?
3. What framework state it expects to work with?

It will take a few hours more to answer this questions.

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
the application actually does.  What problems it is trying to solve?

Most frameworks are busy with forms, serializers, transport layers,
field mappings.  And all these implementation details are not the
right abstractions for decision making.

Usually, our first thought will be moving our business logic from the
view into a function.

.. code:: python

    def buy_subscription(category_id, price_id, user):

        category = find_category(category_id)
        price = find_price(price_id)
        profile = find_profile(user)
        if profile.balance < price.cost:
            raise ValueError
        decrease_balance(profile, price.cost)
        save_profile(profile)
        expires = calculate_period(price.period)
        subscription = create_subscription(profile, category, expires)
        notification = send_notification('subscribe', profile, category)

The author definitely has a few good points to write code this way.

It is short, has clear names and intent.

If you enjoy writing code like this, stop reading and go write it.
I'm serious!

But we see a few disadvantages in it.

1. Growth problem.  In real life, functions like this will have ~50
   lines of code, a lot of variables and nested ``if`` statements.
   Eventually, a programmer will decide to hide its complexity
   somewhere.

   * Convert to the object.  The main intent is hiding ~50 variables
     in ~50 object attributes.  This will improve the readability of
     the main method.  But will harm the understanding of where data
     came from.

   * Mixins.  At some point, we will like to reuse parts of our
     business logic.  A mixin is the most common way to make code with
     classes reusable.  But it will lead to even more implicit source
     of date.  Attributes appear from nowhere.

2. Top-down architecture.  We call functions directly.  They call
   other low level functions directly.  Our business logic has a very
   high coupling with the way we talk to the database, SMS gateway or
   notification server.  This approach has zero flexibility.

There is a better way.

DSL
===

Wouldn't it be nice if we can just read business logic as it was
intended?

.. code:: python

    from stories import story, arguments

    class Subscription:

        @story
        @arguments("category_id", "price_id")
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
      category_id = 1318           # Story argument
      user = <User: 3292>          # Story argument
      category = <Category: 1318>  # Set by Subscription.find_category
    >>> _

Wouldn't it be nice to know which business scenario was executed by
every line in the tests?

.. image:: /static/pytest.png
    :class: with-popup

Wouldn't it be nice to see the same details in the debug toolbar?

.. image:: /static/debug-toolbar.png
    :class: with-popup

Wouldn't it be nice to it when production fails?

.. image:: /static/sentry.png
    :class: with-popup

Interesting, isn't it?  Check out `Definition`_ guide to learn more.

.. _definition: definition.html
