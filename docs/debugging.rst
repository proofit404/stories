===========
 Debugging
===========

There is no perfect code.

Here is the technique we use to debug our own code written with
``stories``.

Code
====

Our regular story looks like this.  `You can read more on this topic
here`_.

.. code:: python

    class ApplyPromoCode:
        """Calculate actual product discount, apply it to the price."""

        @story
        @arguments("category")
        def apply(I):

            I.find_promo_code
            I.check_code_exists
            I.check_expiration
            I.calculate_discount
            I.show_final_price

        # Steps.

        def find_promo_code(self, ctx):

            promo_code = self.load_promo_code(ctx.category)
            return Success(promo_code=promo_code)

        def check_code_exists(self, ctx):

            if not ctx.promo_code:
                return Skip()
            else:
                return Success()

        def check_expiration(self, ctx):

            if ctx.promo_code.is_expired():
                return Skip()
            else:
                return Success()

        def calculate_discount(self, ctx):

            discount = ctx.promo_code.apply_discount(ctx.category.price)
            return Success(discount=discount)

        def show_final_price(self, ctx):

            return Result(ctx.category.price - ctx.discount)

        # Dependencies.

        def __init__(self, load_promo_code):

            self.load_promo_code = load_promo_code


    class Category:

        def __init__(self, price):

            self.price = price


    class PromoCode:

        def __init__(self, percent):

            self.fraction = percent / 100

        def is_expired(self):

            return False

        def apply_discount(self, price):

            return price * self.fraction

It define top level logic without any implementation detail written in
story methods.

We provide an implementation in a separate set of functions.

.. code:: python

    def load_promo_code(category):

        return PromoCode(20)

The first run
=============

Looks good at the first view.  Let's try to run this code.

.. code:: python

    >>> code = ApplyPromoCode(load_promo_code)
    >>> result = code.apply(Category(715))
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "stories/_mounted.py", line 46, in __call__
        return function.execute(runner, ctx, history, self.methods)
      File "stories/_exec/function.py", line 24, in execute
        result = method(ctx)
      File "example.py", line 21, in find_promo_code
        promo_code = self.load_promo_code(ctx.category)
      File "example.py", line 76, in load_promo_code
        return PromoCode(0)
      File "example.py", line 63, in __init__
        self.fraction = 100 / percent
    ZeroDivisionError: division by zero
    >>> _

Oops...  It's broken...

PDB walks in to the bar
=======================

We can read the whole source code, but let’s try to use a debugger
instead! Type this in the same console right after traceback.

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

The second run
==============

Lets fix it.

.. code:: python

    def one(self):

        return 10

And re-run our program.

.. code:: python

    >>> from example import *
    >>> code = ApplyPromoCode(load_promo_code)
    >>> result = code.apply(Category(715))
    >>> result
    1.4
    >>> _

Hooray! It works.

.. _you can read more on this topic here: composition.html#delegate-implementation
