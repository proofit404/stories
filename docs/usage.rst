=======
 Usage
=======

There are several methods to use business object defined with
``@story`` decorator.

Call
====

The most simple variant to execute story, is to call it as regular
method.

Result
------

.. code:: python

    >>> CreateUser().create("John", "john@example.com", 19)
    <User: User object (1)>
    >>> _

TODO: explaine...

Failure
-------

.. code:: python

    >>> CreateUser().create("John", "john@example.com", 17)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "stories/_wrapper.py", line 23, in __call__
        return function.execute(runner, ctx, methods)
      File "stories/_exec/function.py", line 36, in execute
        return runner.got_failure(ctx, method.__name__, result.reason)
      File "stories/_run.py", line 7, in got_failure
        raise FailureError(reason)
    stories.exceptions.FailureError
    >>> _

TODO: explaine...

Run
===

More powerful way to inspect result of the story is to use run instead
of call.

Result
------

.. code:: python

    >>> result = CreateUser().create.run("John", "john@example.com", 19)
    >>> result.is_success
    True
    >>> result.value
    <User: User object (1)>
    >>> _


TODO: explaine...

Failure
-------

.. code:: python

    >>> result = CreateUser().create.run("John", "john@example.com", 17)
    >>> result.is_failure
    True
    >>> result.failed_on("validate")
    True
    >>> result.failed_because("person is too young")
    True
    >>> result.ctx
    CreateUser.create:
      validate (failed: 'person is too young')

    Context:
        name = 'John'               # Story argument
        email = 'john@example.com'  # Story argument
        age = 17                    # Story argument
    >>> result.ctx.age
    17
    >>> _

TODO: explaine...
