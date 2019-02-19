==================
 Failure Protocol
==================

By default, ``Failure`` result has empty ``reason``.

``failed_on`` is the only thing you can do to understand what happened
in the caller code.  You should use the `run story method`_ to have
access to the verbose result.

This is a fragile approach since it depends on method names.  They
tend to change in the future.  Some one can find a better name for a
certain method.  And in some place ``failed_on`` call will not catch
this failure because it's using outdated method name.

Also, one story step can fail for a number of reasons.  For example,
we're making an API call.  We want to process ``401`` and ``403``
error codes differently.  This is where ``failed_on`` method can't
help.

.. note::

   ``Failure protocol`` is the way to allow certain set of values to
   be used as an argument to the ``Failure`` result.

After that in the caller code you can use ``failed_because`` method to
be sure you can understand the exact reason of failure.

List of strings
===============

You can use string literals to mark exact reason of the failure.  In
this case, failure protocol should be collection of all allowed
strings.

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

Enum
====

Composition
===========

Shortcuts
=========

.. _run story method: usage.html#run
