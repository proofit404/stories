
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

.. image:: https://raw.githubusercontent.com/dry-python/brand/master/logo/stories.png

|travis| |codecov| |pyup| |codacy| |pypi| |docs|

----

The business transaction DSL
============================

- `Source Code`_
- `Issue Tracker`_
- `Documentation`_

Installation
------------

All released versions are hosted on the Python Package Index.  You can
install this package with following command.

.. code:: bash

    pip install stories

Usage
-----

``stories`` provide a simple way to define a complex business scenario
that include many processing steps.

.. code:: python

    from stories import story, argument, Success

    class PurchaseProduct:

        @story
        @argument('user')
        @argument('product')
        @argument('shipment_details')
        def purchase(self):

            self.create_order()
            self.calculate_price()
            self.request_payment()
            self.notify_user()

       def create_order(self):

           return Success(
               order=Order.objects.create(
                   user=self.ctx.user,
                   product=self.ctx.product,
               )
           )

This code style allow you clearly separate actual business scenario
from implementation details.

License
-------

Dependencies library is offered under the two clause BSD license.

.. _source code: https://github.com/dry-python/stories
.. _issue tracker: https://github.com/dry-python/stories/issues
.. _documentation: https://stories.readthedocs.io/en/latest/
