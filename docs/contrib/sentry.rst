================
 Sentry contrib
================

This is a picture of the execution path and context variables of the
business object shown in the error report breadcrumbs section:

.. image:: /static/sentry.png
    :class: with-popup

Settings
========

Import this module **before** import any Sentry related stuff:

.. code:: python

    import stories.contrib.sentry.breadcrumbs

Django Settings
===============

If you use Django, you should add this section to your project config
instead of documentation above:

.. code:: python

    SENTRY_CLIENT = "stories.contrib.sentry.django.DjangoClient"
