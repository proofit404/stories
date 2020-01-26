# Debugging

There is no perfect code.

Here is the technique we use to debug our own code written with
`stories`.

## Code

Our regular story looks like this. [You can read more on this topic
here](composition.md#delegate-implementation).

```pycon

>>> from stories import story, arguments, Success, Skip, Result

>>> class ApplyPromoCode:
...     """Calculate actual product discount, apply it to the price."""
...
...     @story
...     @arguments("category_id")
...     def apply(I):
...
...         I.find_category
...         I.find_promo_code
...         I.check_expiration
...         I.calculate_discount
...         I.show_final_price
...
...     # Steps.
...
...     def find_category(self, ctx):
...
...         ctx.category = self.load_category(ctx.category_id)
...         return Success()
...
...     def find_promo_code(self, ctx):
...
...         ctx.promo_code = self.load_promo_code(ctx.category)
...         return Success()
...
...     def check_expiration(self, ctx):
...
...         if ctx.promo_code.is_expired():
...             return Skip()
...         else:
...             return Success()
...
...     def calculate_discount(self, ctx):
...
...         ctx.discount = ctx.promo_code.apply_discount(ctx.category.price)
...         return Success()
...
...     def show_final_price(self, ctx):
...
...         return Result(ctx.category.price - ctx.discount)
...
...     # Dependencies.
...
...     def __init__(self, load_category, load_promo_code):
...
...         self.load_category = load_category
...         self.load_promo_code = load_promo_code

>>> class Category:
...
...     def __init__(self, price=None, name=None, **kwargs):
...
...         self.price = price
...         self.name = name
...         for k, v in kwargs.items():
...             setattr(self, k, v)

>>> class PromoCode:
...
...     def __init__(self, percent):
...
...         self.fraction = percent / 100
...
...     def is_expired(self):
...
...         return False
...
...     def apply_discount(self, price):
...
...         return price * self.fraction

```

It defines top-level logic without any implementation detail written in
story methods.

We provide an implementation in a separate set of functions.

```pycon

>>> def load_category(category_id):
...     return Category(orice=715, category_id=category_id)

>>> def load_promo_code(category):
...     return PromoCode(percent=5)

```

## The first run

Looks good at the first view. Isn't it? Let's try to run this code.

```pycon

>>> promo_code = ApplyPromoCode(load_category, load_promo_code)

>>> result = promo_code.apply(category_id=1024)
Traceback (most recent call last):
  ...
TypeError: unsupported operand type(s) for *: 'NoneType' and 'float'

```

Oops... It's broken...

## PDB walks into the bar

We can take the magnifying glass and read through the whole source code
meticulously.

But let’s try to use a debugger instead! Type this in the same console
right after traceback.

```pycon

>>> import pdb

>>> pdb.pm()
> example.py(73)apply_discount()
-> return price * self.fraction
(Pdb) ll
 71      def apply_discount(self, price):
 72
 73  ->      return price * self.fraction
(Pdb) args
self = <example.PromoCode>
price = None

```

It's clear it isn't our fault. Someone passes a wrong value to us. We'll
go one frame upper in the call stack and look who does it.

```pycon

(Pdb) up
> example.py(38)calculate_discount()
-> discount = ctx.promo_code.apply_discount(ctx.category.price)

(Pdb) ll
 36      def calculate_discount(self, ctx):
 37
 38  ->      ctx.discount = ctx.promo_code.apply_discount(ctx.category.price)
 39          return Success()

```

We can clearly see that the `price` attribute of the `category` context
variable is `None`. But who set it this way? `PDB` has no answer to
that.

At this point usually, you will re-run the whole process to stop
debugger earlier trying to find the place in your code where this `None`
was defined.

But fortunately, we're using `stories`! Its context has the full
support of the introspection.

Let's print story context at the moment of the failure.

```pycon

(Pdb) p ctx
ApplyPromoCode.apply
  find_category
  find_promo_code
  check_expiration
  calculate_discount (errored: TypeError)

Context:
  category_id = 1024                # Story argument
  category = <example.Category>     # Set by ApplyPromoCode.find_category
  promo_code = <example.PromoCode>  # Set by ApplyPromoCode.find_promo_code

```

We can tell that `category` was defined by `find_category` step. Let's
take a closer look at it.

```pycon

>>> def find_category(self, ctx):
...     ctx.category = self.load_category(ctx.category_id)
...     return Success()

```

What are the `load_category` stands for?

```pycon

(Pdb) p self.load_category
<function load_category>

(Pdb) p dir(ctx.category)
['category_id', 'name', 'orice', 'price']

```

These `orice` and `price` attribute looks suspicious.

```pycon

>>> def load_category(category_id):
...     return Category(orice=715, category_id=category_id)
...     #               `---- Root of all evil.

```

So we can quickly find mistyped argument name in the `Category`
constructor.

## The second run

Let's fix it.

```pycon

>>> def load_category(category_id):
...     return Category(price=715, category_id=category_id)

```

And re-run our program.

```pycon

>>> promo_code = ApplyPromoCode(load_category, load_promo_code)

>>> result = promo_code.apply(category_id=1024)

>>> result
679.25

```

Hooray! It works.
