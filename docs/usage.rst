=======
 Usage
=======

There are several methods to use business object defined with the
``@story`` decorator.

Call
====

The most simple variant to execute story is to call it as a regular
method.

Result
------

.. code:: python

    >>> Subscription().buy(category_id=1, price_id=1, user_id=1)
    <Category: Category object (1)>
    >>> _

The story was executed successfully.  It returns an object we put into
``Result`` marker.

Failure
-------

.. code:: python

    >>> Subscription().buy(category_id=2, price_id=2, user_id=1)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "stories/_wrapper.py", line 23, in __call__
        return function.execute(runner, ctx, methods)
      File "stories/_exec/function.py", line 36, in execute
        return runner.got_failure(ctx, method.__name__, result.reason)
      File "stories/_run.py", line 7, in got_failure
        raise FailureError(reason)
    stories.exceptions.FailureError()
    >>> _

Story failed.  The user does not have enough money to complete this
purchase.  ``Failure`` marker throws an exception when ``call`` method
was used.

Run
===

A more powerful way to inspect the result of the story is to use the
``run`` method instead.

The ``run`` method always returns an object.  This object contains a
summary of the business object execution.

Result
------

.. code:: python

    >>> result = Subscription().buy.run(category_id=1, price_id=1, user_id=1)
    >>> result.is_success
    True
    >>> result.value
    <Category: Category object (1)>
    >>> _

If the story was executed successfully, its actual result will be
available in the ``value`` attribute.

Failure
-------

.. code:: python

    >>> result = Subscription().buy.run(category_id=2, price_id=2, user_id=1)
    >>> result.is_failure
    True
    >>> result.failed_on("check_balance")
    True
    >>> result.failed_because("low_balance")
    True
    >>> result.ctx
    Subscription.buy:
      find_category
      find_price
      find_profile
      check_balance (failed: 'low_balance')

    Context:
      category_id = 2                            # Story argument
      price_id = 2                               # Story argument
      user = <User: User object (7)>             # Story argument
      category = <Category: Category object (2)> # Set by Subscription.find_category
      price = <Price: Price object (2)>          # Set by Subscription.find_price
      profile = <Profile: Profile object (7)>    # Set by Subscription.find_profile
    >>> result.ctx.profile.balance
    20
    >>> result.ctx.price.cost
    73
    >>> _

``run`` does not raise an error.  Even if the story returns
``Failure`` marker.  Instead, you can use methods like ``failed_on``
and ``failed_because`` to look for failed story method and exact
reason.  The context of the failed story is also available in the result
object.
