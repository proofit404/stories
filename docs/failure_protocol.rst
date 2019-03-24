==================
 Failure Protocol
==================

By default, ``Failure`` result has an empty ``reason``.

``failed_on`` is the only thing you can do to understand what happened
in the caller code.  You should use the `run the story method`_ to
have access to the verbose result.

This is a fragile approach since it depends on method names.  They
tend to change in the future.  Someone can find a better name for a
certain method.  And in some place, the ``failed_on`` call will not
catch this failure because it's using an outdated method name.

Also, one story step can fail for a number of reasons.  For example,
we're making an API call.  We want to process ``401`` and ``403``
error codes differently.  This is where ``failed_on`` method can't
help.

.. note::

   ``Failure protocol`` is the way to allow a certain set of values to
   be used as an argument to the ``Failure`` result.

After that in the caller code, you can use the ``failed_because``
method to be sure you can understand the exact reason for failure.

List of strings
===============

You can use string literals to mark the exact reason for the
failure.  In this case, failure protocol should be a collection of all
allowed strings.

.. code:: python

    class ApplyPromoCode:
        """Calculate actual product discount, apply it to the price."""

        @story
        @arguments("category")
        def apply(I):

            I.find_promo_code
            I.check_promo_code_exists
            I.check_expiration

        # Steps.

        def find_promo_code(self, ctx):

            promo_code = self.load_promo_code(ctx.category)
            return Success(promo_code=promo_code)

        def check_promo_code_exists(self, ctx):

            if ctx.promo_code is None:
                return Failure("not_found")
            else:
                return Success()

        def check_expiration(self, ctx):

            if ctx.promo_code.is_expired():
                return Failure("expired")
            else:
                return Success()

    # Protocol definition.

    ApplyPromoCode.apply.failures(["not_found", "expired"])

Now you can use these string literals to process different failures in
a different way.

.. code:: pycon

    >>> promo_code = ApplyPromoCode()
    >>> result = promo_code.apply.run(category=Category(177))
    >>> if result.is_success:
    ...     print("Promo code applied")
    ... elif result.failed_because("not_found"):
    ...     print("Promo code not found")
    ... elif result.failed_because("expired"):
    ...     print("Promo code expired")
    Promo code not found
    >>> _

Enum
====

You can use `enum`_ members to mark the exact reason for the failure.
In this case, failure protocol should be `enum`_ subclass.

.. code:: python

    from enum import Enum, auto

    class ApplyPromoCode:
        """Calculate actual product discount, apply it to the price."""

        @story
        @arguments("category")
        def apply(I):

            I.find_promo_code
            I.check_promo_code_exists
            I.check_expiration

        # Steps.

        def find_promo_code(self, ctx):

            promo_code = self.load_promo_code(ctx.category)
            return Success(promo_code=promo_code)

        def check_promo_code_exists(self, ctx):

            if ctx.promo_code is None:
                return Failure(Errors.not_found)
            else:
                return Success()

        def check_expiration(self, ctx):

            if ctx.promo_code.is_expired():
                return Failure(Errors.expired)
            else:
                return Success()

    # Protocol definition.

    @ApplyPromoCode.apply.failures
    class Errors(Enum):

        not_found = auto()
        expired = auto()

On Python 2 you can use `enum34`_ package::

    pip install enum34

Now you can use `enum`_ members to process different failures in a
different way.

.. code:: pycon

    >>> promo_code = ApplyPromoCode()
    >>> result = promo_code.apply.run(category=Category(177))
    >>> if result.is_success:
    ...     print("Promo code applied")
    ... elif result.failed_because(promo_code.apply.failures.not_found):
    ...     print("Promo code not found")
    ... elif result.failed_because(promo_code.apply.failures.expired):
    ...     print("Promo code expired")
    Promo code not found
    >>> _

When you `run the story method`_ the actual failure protocol is
available under ``failures`` property of that story method.  So there
is no need to import ``Errors`` class in the caller code.

Composition
===========

Failure protocols of parent and sub-story often mismatch.  There is a
good reason for that.  Indeed they usually describe rules at different
levels of abstraction.  Failure of sub-story can tell us about some
low-level error.  And the failure of the parent story usually tells us
something about high-level business rules violation.

.. note::

    A story in the composition can return failures with only reasons
    match its own protocol.

.. code:: python

    class Subscription:

        @story
        def buy(I):

            I.find_promo_code
            I.check_balance
            I.persist_payment
            I.show_category

        # Steps.

        def check_balance(self, ctx: "Context"):

            if ctx.user.balance < ctx.category.price:
                return Failure(self.Errors.low_balance)
            else:
                return Success()

        # Protocols.

        @buy.failures
        class Errors(Enum):

            low_balance = auto()

        # Dependencies.

        def __init__(self, find_promo_code):

            self.find_promo_code = find_promo_code

    class PromoCode:

        @story
        def find(I):

            I.find_token
            I.check_expiration
            I.calculate_discount

        # Steps.

        def check_expiration(self, ctx: "Context"):

            if ctx.token.is_expired():
                return Failure(self.Errors.expired)
            else:
                return Success()

        # Protocols.

        @find.failures
        class Errors(Enum):

            expired = auto()

A composition of these two stories can fail both because of
``low_balance`` and ``expired`` reasons.  For convenience,
``failures`` property will contain protocols composition.  A new
``enum`` class.

.. code:: pycon

    >>> buy_subscription = Subscription(PromoCode().find).buy
    >>> result = buy_subscription.run()
    >>> if result.is_success:
    ...     print("Subscribed")
    ... elif result.failed_because(buy_subscription.failures.low_balance):
    ...     print("Low balance")
    ... elif result.failed_because(buy_subscription.failures.expired):
    ...     print("Promo code expired")
    Promo code expired
    >>> _

This composition rule works both for `class methods`_ with inheritance
and `instance attributes`_ with dependency injection.

Shortcuts
=========

If you use `sub-stories with inheritance`_, your class will usually
contain multiple story definitions.

.. code:: python

    class Subscription:

        @story
        @arguments("category_id", "price_id", "user_id")
        def buy(I):

            I.find_category
            I.find_promo_code
            I.check_balance

        @story
        @arguments("category", "price")
        def find_promo_code(I):

            I.find_token
            I.check_expiration
            I.calculate_discount

You can specify failure protocol for each story using a stack of
decorators.

.. code:: python

    @Subscription.buy.failures
    @Subscription.find_promo_code.failures
    class Errors(Enum):

        forbidden = auto()
        not_found = auto()

But instead of this, we encourage you to use a simple shortcut
function.

.. code:: python

    from stories.shortcuts import failures_in

    failures_in(Subscription, ["forbidden", "not_found"])

    @failures_in(Subscription)
    class Errors(Enum):

        forbidden = auto()
        not_found = auto()

.. _run the story method: usage.html#run
.. _enum: https://docs.python.org/3/library/enum.html
.. _enum34: https://pypi.org/project/enum34/
.. _sub-stories with inheritance: composition.html#class-methods
.. _class methods: composition.html#class-methods
.. _instance attributes: composition.html#instance-attributes
