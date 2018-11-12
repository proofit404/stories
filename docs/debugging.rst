===========
 Debugging
===========

There is no perfect code.

Here is the technique we use to debug our own code written with
``stories``.

Code
====

Our regular story looks like this.

.. code:: python

    class Action:

        @story
        @argument("value")
        def do(I):

            I.one
            I.two
            I.three
            I.four

        def one(self, ctx):

            var_a = self.impl.one()
            return Success(var_a=var_a)

        def two(self, ctx):

            var_b = self.impl.two(ctx.value, ctx.var_a)
            return Success(var_b=var_b)

        def three(self, ctx):

            var_c = self.impl.three(ctx.var_b)
            return Success(var_c=var_c)

        def four(self, ctx):

            return Result(ctx.var_c)

        def __init__(self, impl):

            self.impl = impl

It define top level logic without any implementation detail written in
story methods.

We provide implementation in a separate class.

.. code:: python

    class Implementation:

        def one(self):

            return 0

        def two(self, a, b):

            return a / b

        def three(self, a):

            return a * 2

The first run
=============

Looks good at the first view.  Let's try to run this code.

.. code:: python

    >>> action = Action(impl=Implementation())
    >>> result = action.do(value=7)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "stories/_wrapper.py", line 23, in __call__
        return function.execute(runner, ctx, methods)
      File "stories/_exec/function.py", line 23, in execute
        result = method(obj, ctx)
      File "example.py", line 21, in two
        var_b = self.impl.two(ctx.value, ctx.var_a)
      File "example.py", line 45, in two
        return a / b
    ZeroDivisionError: integer division or modulo by zero
    >>> _

Oops...  It's broken...

PDB walks in to the bar
=======================

We can read the whole source code, but let's try to use debugger
instead!

.. code:: python

    >>> import pdb
    >>> pdb.pm()
    > /home/proofit404/data/stories/src/example.py(45)two()
    -> return a / b
    (Pdb) ll
     43  	    def two(self, a, b):
     44
     45  ->	        return a / b
    (Pdb) args
    self = <example.Implementation object at 0x7feb8b699198>
    a = 7
    b = 0
    (Pdb) _

It's clear it isn't our fault.  Some one passes wrong value to us.

At this point you usually will re-run the whole process to stop
debugger earlier trying to find the place in your code where this zero
was defined.

But hopefully we use ``stories``!  It's context has full support of
the introspection.

We'll go one frame upper in the call stack and print story context at
the moment of the failure.

.. code:: python

    (Pdb) up
    > example.py(21)two()
    -> var_b = self.impl.two(ctx.value, ctx.var_a)
    (Pdb) ll
     19  	    def two(self, ctx):
     20
     21  ->	        var_b = self.impl.two(ctx.value, ctx.var_a)
     22  	        return Success(var_b=var_b)
    (Pdb) p ctx
    Action.do:
      one
      two (errored: ZeroDivisionError)

    Context:
      value = 7  # Story argument
      var_a = 0  # Set by Action.one
    (Pdb) _

We can clearly see who set the wrong value.

``Action.one`` set it to the context.

So we can quickly find mistyped return value in the
``Implementation.one``.

Lets fix it.

.. code:: python

    def one(self):

        return 10

And re-run our program.

.. code:: python

    >>> from example import *
    >>> action = Action(impl=Implementation())
    >>> result = action.do(value=7)
    >>> result
    1.4
    >>> _

Hooray! It works.
