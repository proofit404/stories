Sometimes high-level wrapping stories consist from inner stories completely. In
that case it's tedious to copy-paste steps definition into constructor
arguments. To reduce level of boilerplace code in such cases, stories library
provides `@initiate` decorator.

## All story steps would be used in class constructor arguments

When you decorate story class with `@initiate` decorator, in addition to the
`__call__` method it would add `__init__` method as well. Story steps would be
used as names for constructor arguments.

=== "`@initiate`"

    ```pycon

    >>> from stories import Story, I, initiate

    >>> @initiate
    ... class Purchase(Story):
    ...     I.find_order
    ...     I.find_customer
    ...     I.persist_payment

    ```

=== "`__init__`"

    ```pycon

    >>> from stories import Story, I

    >>> class Purchase(Story):
    ...     I.find_order
    ...     I.find_customer
    ...     I.persist_payment
    ...
    ...     def __init__(self, find_order, find_customer, persist_payment):
    ...         self.find_order = find_order
    ...         self.find_customer = find_customer
    ...         self.persist_payment = persist_payment

    ```

## Only `Story` subclasses could be initiated

Classes decorated by `@initiate` function should be subclasess of the `Story`.
Otherwise, there is no steps to operate on.

```pycon

>>> @initiate
... class Purchase:
...     def find_order(self, state):
...         state.order = self.load_order(state.order_id)
...
...     def find_customer(self, state):
...         state.customer = self.load_customer(state.customer_id)
...
...     def persist_payment(self, state):
...         self.create_payment(state.order_id, state.customer_id)
Traceback (most recent call last):
  ...
_stories.exceptions.StoryError: @initiate can decorate Story subclasses only

```

## Initiated `Story` class should not have step methods

`@initiate` decorator does not allow to mix step methods with nested stories on
initiated classes. Usually, story steps defined by methods expects some
additional dependencies to be passed in the constructor.

```pycon

>>> from stories import Story, I, initiate

>>> @initiate
... class Purchase(Story):
...     I.find_order
...     I.find_customer
...     I.persist_payment
...
...     def find_order(self, state):
...         state.order = self.load_order(state.order_id)
Traceback (most recent call last):
  ...
_stories.exceptions.StoryError: Story decorated by @initiate can not have step methods

```

## Initiated `Story` class should not have constructor

```pycon

>>> from stories import Story, I, initiate

>>> @initiate
... class Purchase(Story):
...     I.find_order
...     I.find_customer
...     I.persist_payment
...
...     def __init__(self):
...         ...
Traceback (most recent call last):
  ...
_stories.exceptions.StoryError: Story decorated by @initiate can not have constructor defined

```
