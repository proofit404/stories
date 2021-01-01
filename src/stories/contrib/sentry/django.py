"""This module contains integration with Sentry for Django framework."""
from raven.contrib.django.client import DjangoClient


__all__ = ["DjangoClient"]
