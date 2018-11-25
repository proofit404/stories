
.. |travis| image:: https://travis-ci.org/dry-python/stories.svg?branch=master
    :target: https://travis-ci.org/dry-python/stories

.. |codecov| image:: https://codecov.io/gh/dry-python/stories/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/dry-python/stories

.. |pyup| image:: https://pyup.io/repos/github/dry-python/stories/shield.svg
     :target: https://pyup.io/repos/github/dry-python/stories/

.. |codacy| image:: https://api.codacy.com/project/badge/Grade/bd0a5736bc2f43d6b3fcbf3803d50f9b
    :target: https://www.codacy.com/app/dry-python/stories/

.. |pypi| image:: https://img.shields.io/pypi/v/stories.svg
    :target: https://pypi.python.org/pypi/stories/

.. |docs| image:: https://readthedocs.org/projects/stories/badge/?version=latest
    :target: https://stories.readthedocs.io/en/latest/?badge=latest

.. |gitter| image:: https://badges.gitter.im/dry-python/stories.svg
    :target: https://gitter.im/dry-python/stories

.. image:: https://raw.githubusercontent.com/dry-python/brand/master/logo/stories.png

|travis| |codecov| |pyup| |codacy| |pypi| |docs| |gitter|

----

The business transaction DSL
============================

``stories`` is a business transaction DSL.  It provides a simple way
to define a complex business transaction that includes processing over
many steps and by many different objects.  It makes error handling a
primary concern by taking a “`Railway Oriented Programming`_” approach
to capturing and returning errors from any step in the transaction.

``stories`` is based on the following ideas:

* A business transaction is a series of operations where any can fail
  and stop the processing.

* A business transaction can describe its steps on an abstract level
  without being coupled to any details about how individual operations
  work.

* A business transaction doesn’t have any state.

* Each operation shouldn’t accumulate state, instead it should receive
  an input and return an output without causing any side-effects.

* The only interface of an operation is ``ctx``.

* Each operation provides a meaningful piece of functionality and can
  be reused.

* Errors in any operation should be easily caught and handled as part
  of the normal application flow.

Example
=======

``stories`` provide a simple way to define a complex business scenario
that include many processing steps.

.. code:: python

    from stories import story, argument, Success

    class PurchaseProduct:

        @story
        @argument('user')
        @argument('product')
        @argument('shipment_details')
        def purchase(I):

            I.create_order
            I.calculate_price
            I.request_payment
            I.notify_user

        def create_order(self, ctx):

            order = Order.objects.create(
                user=ctx.user,
                product=ctx.product
            )
            return Success(order=order)

        def calculate_price(self, ctx):

            return Success(...

This code style allow you clearly separate actual business scenario
from implementation details.

Note
====

``stories`` library was heavily inspired by dry-transaction_ ruby
gem.

Contents
========

.. toctree::
    :maxdepth: 2

    why
    definition
    usage
    execution
    debugging
    composition
    contrib/index
    faq

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _railway oriented programming: http://fsharpforfunandprofit.com/rop/
.. _dry-transaction: http://dry-rb.org/gems/dry-transaction/
