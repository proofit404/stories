=================
 Execution rules
=================

There are some rules on how stories are executed:

* Methods called in the order as they written in the story

.. code:: python

    class Action:

        @story
        def do(I):

            I.one
            I.two
            I.three

        def one(self, ctx):

            print("one")
            return Success()

        def two(self, ctx):

            print("two")
            return Success()

        def three(self, ctx):

            print("three")
            return Success()

.. code:: python

    >>> Action().do()
    one
    two
    three
    >>> _

* If the story calls another story in its body, methods of this
  sub-story add to the caller in the order they occur in sub-story
  body.

.. code:: python

    class Action:

        @story
        def do(I):

            I.one
            I.sub
            I.four

        @story
        def sub(I):

            I.two
            I.three

        def one(self, ctx):

            print("one")
            return Success()

        def two(self, ctx):

            print("two")
            return Success()

        def three(self, ctx):

            print("three")
            return Success()

        def four(self, ctx):

            print("four")
            return Success()

.. code:: python

    >>> Action().do()
    one
    two
    three
    four
    >>> _

* Each story method should return an instance of ``Success``,
  ``Failure``, ``Result`` or ``Skip`` classes.

* If story method return ``Success`` execution of the whole story
  continues from the next step.

* Story method can use ``Success`` keyword arguments to set some
  context variables for future methods.

.. code:: python

    class Action:

        @story
        def do(I):

            I.one
            I.two

        def one(self, ctx):

            return Success(var=1)

        def two(self, ctx):

            print(ctx.var)
            return Success()

.. code:: python

    >>> Action().do()
    1
    >>> _

* If story method return ``Failure``, the whole story considered
  failed.  Execution stops at this point.

.. code:: python

    class Action:

        @story
        def do(I):

            I.one
            I.two

        def one(self, ctx):

            print("one")
            return Failure()

        def two(self, ctx):

            print("two")
            return Success()

.. code:: python

    >>> Action().do()
    one
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "stories/_wrapper.py", line 23, in __call__
        return function.execute(runner, ctx, methods)
      File "stories/_exec/function.py", line 33, in execute
        return runner.got_failure(ctx, method.__name__, result.reason)
      File "stories/_run.py", line 7, in got_failure
        raise FailureError(reason)
    stories.exceptions.FailureError
    >>> _

* ``Failure`` of the sub-story will fail the whole story.

* If the story method return ``Result``, the whole story considered
  done.  The argument passed to the ``Result`` constructor will be the
  return value of the story call.

* The ``Result`` of the sub-story will be the result of the whole
  story.

* If sub-story method return ``Skip`` result, execution will be
  continued form the next method of the caller story.

* If the topmost story return ``Skip`` result, execution will end.
