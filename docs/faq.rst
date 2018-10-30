============================
 Frequently asked questions
============================

Here we'll try to explain some reasons behind our decisions.

Why it is too magic?
====================

Careful programmers tend to avoid tools built on top of
meta-programming.  But we still use tools like dataclasses_, attrs_
and `django orm`_ because they improve developer experience a lot.

This is what ``stories`` tries very hard:

    Bring the maximum value to your process, while keeping magic at
    the lowest possible minimum.

Why DSL does not use inheritance?
=================================

Many tools use like object relation mappers, web frameworks and task
queues use inheritance from some base class as the core of API.  We
saw a few problems with this approach.

First of all, you tend to put your business logic inside this
subclasses.  Fighting this evil was the initial idea behind
``stories`` library.

Also, this approach restricts your possibilities to manage your own
classes.  We want you to be free at the decisions where to put story
definition anywhere.  It is your right to place it inside Django
Model.

Why we need ``@argument`` decorator instead of function arguments?
==================================================================

For the simplicity of implementation inside ``@story`` decorator.

Can I use ``self`` instead of ``I`` argument?
=============================================

Yes, you are free to use whatever name you want.  But we keep this
convention in our documentation and examples to keep in mind that
``I``, ``self`` and ``ctx`` are three different things.

.. _dataclasses: https://docs.python.org/3/library/dataclasses.html
.. _attrs: https://www.attrs.org/
.. _django orm: https://docs.djangoproject.com/en/dev/topics/db/
