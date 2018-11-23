=======
 Usage
=======

Technically speaking, a story is a method of the class which calls
other methods of this class in special order.

The body of the story isn't executed directly.  It's used as a spec of
what should happen and when.

Stories called as usual methods.  First of all, it will build spec of
methods using its body.  Then it will call methods of this class
according to this spec.  This happens outside of the story body.  Each
method is called with special execution context.

Basic definition
================

This is example will be used for simplicity to show basic rules of
stories.  Real world examples will be way more complex, but still
defined by rules explained here.

.. code:: python

    from stories import argument, story, Success, Result, Failure

    class CreateUser:

        @story
        @argument("name")
        @argument("email")
        @argument("age")
        def create(I):

            I.validate
            I.persist
            I.send_confirmation_email
            I.show_user

        # Steps.

        def validate(self, ctx):

            if ctx.age < 18:
                return Failure("person is too young")
            return Success()

        def persist(self, ctx):

            user = User.objects.create(name=ctx.name)
            return Success(user=user)

        def send_confirmation_email(self, ctx):

            body = welcome_text(ctx.user)
            send_email(ctx.email, body)
            return Success()

        def show_user(self, ctx):

            return Result(ctx.user)

Calling the story
=================

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

Running the story
=================

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
