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
        def do(I):

            I.one
            I.two
            I.three
            I.four

        def one(self, ctx):

            var_a = self.impl.one()
            return Success(var_a=var_a)

        def two(self, ctx):

            var_b = self.impl.two()
            return Success(var_b=var_b)

        def three(self, ctx):

            var_c = self.impl.three()
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

            return 1

        def two(self):

            return 2

        def three(self):

            return 3

The first run
=============
