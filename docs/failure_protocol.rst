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

.. code:: python

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

.. code:: python

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

Shortcuts
=========

.. _run the story method: usage.html#run
.. _enum: https://docs.python.org/3/library/enum.html
.. _enum34: https://pypi.org/project/enum34/
