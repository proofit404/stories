.. |travis| image:: https://travis-ci.org/dry-python/stories.svg?branch=master
    :target: https://travis-ci.org/dry-python/stories

.. |codecov| image:: https://codecov.io/gh/dry-python/stories/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/dry-python/stories

.. |docs| image:: https://readthedocs.org/projects/stories/badge/?version=latest
    :target: https://stories.readthedocs.io/en/latest/?badge=latest

.. |gitter| image:: https://badges.gitter.im/dry-python/stories.svg
    :target: https://gitter.im/dry-python/stories

.. |pypi| image:: https://img.shields.io/pypi/v/stories.svg
    :target: https://pypi.python.org/pypi/stories/

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black

.. image:: https://raw.githubusercontent.com/dry-python/brand/master/logo/stories.png

|travis| |codecov| |docs| |gitter| |pypi| |black|

----

The business transaction DSL
============================

- `Source Code`_
- `Issue Tracker`_
- `Documentation`_
- `Discussion`_

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

    from stories import story, arguments, Success, Failure, Result

    class Subscribe:

        @story
        @arguments('category_id', 'user_id')
        def buy(I):

            I.find_category
            I.find_profile
            I.check_balance
            I.persist_subscription
            I.show_subscription

        def find_category(self, ctx):

            category = Category.objects.get(id=ctx.category_id)
            return Success(category=category)

        def find_profile(self, ctx):

            profile = Profile.objects.get(user_id=ctx.user_id)
            return Success(profile=profile)

        def check_balance(self, ctx):

            if ctx.category.cost < ctx.profile.balance:
                return Success()
            else:
                return Failure()

        def persist_subscription(self, ctx):

            subscription = Subscription(ctx.category, ctx.profile)
            subscription.save()
            return Success(subscription=subscription)

        def show_subscription(self, ctx):

            return Result(ctx.subscription)

.. code:: python

    >>> Subscribe().buy(category_id=1, user_id=1)
    <Subscription object>
    >>> _

This code style allow you clearly separate actual business scenario
from implementation details.

License
-------

Stories library is offered under the two clause BSD license.

.. _source code: https://github.com/dry-python/stories
.. _issue tracker: https://github.com/dry-python/stories/issues
.. _documentation: https://stories.readthedocs.io/en/latest/
.. _discussion: https://gitter.im/dry-python/stories
