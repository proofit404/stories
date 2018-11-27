=========
 Contrib
=========

This section of the documentation describes ``stories`` integration
with common tools for development, testing, and monitoring.  This
allows you to see useful information from the Context in lots of
cases.  Otherwise, you'll spend your precious time to get this
information yourself.

Py.test
=======

Py.test is a state of art testing tool for Python.  `pytest`_ contrib
gives you an ability to see the execution path and context variables
of each line of the failing test.

Debug Toolbars
==============

`Debug toolbar`_ is the most common way to get information about
request-response life-circle in a huge amount of web frameworks.
``stories`` add execution path and context variables of all business
objects ran in this request processing.  See how easy it is to install
it for `Django`_.

Sentry
======

`Sentry`_ is a popular error tracking platform.  ``stories`` contrib
add execution path and context variables of the business object to the
breadcrumbs section.  You will see this useful information attached to
the error report.  This information is also available in local
variables of each traceback frame.

Contents
========

.. toctree::
    :maxdepth: 2

    pytest
    debug_toolbars
    sentry

.. _pytest: pytest.html
.. _debug toolbar: debug_toolbars.html
.. _django: debug_toolbars.html#django-contrib
.. _sentry: sentry.html
