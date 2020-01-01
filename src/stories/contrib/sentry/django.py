"""
stories.contrib.sentry.django
-----------------------------

This module contains integration with Sentry for Django framework.

:copyright: (c) 2018-2020 dry-python team.
:license: BSD, see LICENSE for more details.
"""
from raven.contrib.django.client import DjangoClient


__all__ = ["DjangoClient"]
