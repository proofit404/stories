================
 Debug Toolbars
================

Many frameworks provide debug toolbar add-ons.  ``stories`` integrate
with these toolbars to show the execution path and context variables
of all business objects triggered by the framework handler.

Django contrib
==============

Add this lines to your developer's settings:

.. code:: python

    from debug_toolbar.settings import PANELS_DEFAULTS

    INSTALLED_APPS = [
        "debug_toolbar",
        "stories.contrib.debug_toolbars.django",
        ...,
    ]

    MIDDLEWARE = [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
        ...,
    ]

    DEBUG_TOOLBAR_PANELS = PANELS_DEFAULTS + [
        "stories.contrib.debug_toolbars.django.panels.StoriesPanel"
    ]

You should see ``stories`` panel in your debug toolbar:

.. image:: /static/debug-toolbar.png
    :class: with-popup
