# @initiate

Sometimes high-level wrapping stories consist from inner stories completely. In
that case it's tedious to copy-paste steps definition into constructor
arguments. To reduce level of boilerplace code in such cases, stories library
provides `@initiate` decorator.

## Principles

- [All story steps would be used in class constructor arguments](#all-story-steps-would-be-used-in-class-constructor-arguments)

### All story steps would be used in class constructor arguments

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

    >>> @initiate
    ... class Purchase(Story):
    ...     I.find_order
    ...     I.find_customer
    ...     I.persist_payment
    ...
    ...     def __init__(self, find_order, find_customer, persist_payment):
    ...         self.find_order = find_order
    ...         self.find_customer = find_customer
    ...         self.persist_payment = persist_payment

    ```

<p align="center">&mdash; ⭐ &mdash;</p>
<p align="center"><i>The <code>stories</code> library is part of the SOLID python family.</i></p>
