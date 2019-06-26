# Sentry contrib

This is a picture of the execution path and context variables of the
business object shown in the error report breadcrumbs section:

![image](/static/sentry.png)

## Settings

Import this module **before** import any Sentry related stuff:

```python
import stories.contrib.sentry.breadcrumbs
```

## Django Settings

If you use Django, you should add this section to your project config
instead of the import statement documented above:

```python
SENTRY_CLIENT = "stories.contrib.sentry.django.DjangoClient"
```
