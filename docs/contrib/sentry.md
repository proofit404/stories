# Sentry contrib

This is a picture of the execution path and context variables of the
business object shown in the error report breadcrumbs section:

![Sentry Breadcrumbs](https://raw.githubusercontent.com/dry-python/dry-python.github.io/develop/slides/pics/sentry.png)

## Settings

Import this module **before** import any Sentry related stuff:

```pycon

>>> import stories.contrib.sentry

```

## Django Settings

If you use Django, you should add this section to your project config
instead of the import statement documented above:

```pycon

>>> SENTRY_CLIENT = "stories.contrib.sentry.django.DjangoClient"

```
