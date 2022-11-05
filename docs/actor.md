# Actor

## Principles

- [Story could define an actor](#story-could-define-an-actor)

### Story could define an actor

Complicated business process is always a composition of smaller business
processes. Sometimes these smaller processes would be executed by different
persons in real life. Or by people with different roles. To make it easier for
the reader of your code to understand who is `I` in current story you could
define an actor as part of the story class.

Our general advice would be **always** define story actors even if you system
only has single role at the moment. This small change would give right context
for the reader. And please **do not call it User**. It is always a user.

=== "sync"

    ```pycon

    >>> from dataclasses import dataclass
    >>> from types import SimpleNamespace
    >>> from typing import Callable
    >>> from stories import Story, I, Actor
    >>> from app.repositories import load_order, load_customer, create_payment

    >>> class Customer(Actor):
    ...     ...

    >>> @dataclass
    ... class Purchase(Story, Customer):
    ...     I.find_order
    ...     I.find_customer
    ...     I.check_balance
    ...     I.persist_payment
    ...
    ...     def find_order(self, state):
    ...         state.order = self.load_order(state.order_id)
    ...
    ...     def find_customer(self, state):
    ...         state.customer = self.load_customer(state.customer_id)
    ...
    ...     def check_balance(self, state):
    ...         if not state.order.affordable_for(state.customer):
    ...             raise Exception
    ...
    ...     def persist_payment(self, state):
    ...         state.payment = self.create_payment(
    ...             order_id=state.order_id, customer_id=state.customer_id
    ...         )
    ...
    ...     load_order: Callable
    ...     load_customer: Callable
    ...     create_payment: Callable

    >>> purchase = Purchase(
    ...     load_order=load_order,
    ...     load_customer=load_customer,
    ...     create_payment=create_payment,
    ... )

    >>> state = SimpleNamespace(order_id=1, customer_id=1)

    >>> purchase(state)

    ```

=== "async"

    ```pycon

    >>> import asyncio
    >>> from dataclasses import dataclass
    >>> from types import SimpleNamespace
    >>> from typing import Coroutine
    >>> from stories import Story, I, Actor
    >>> from aioapp.repositories import load_order, load_customer, create_payment

    >>> class Customer(Actor):
    ...     ...

    >>> @dataclass
    ... class Purchase(Story, Customer):
    ...     I.find_order
    ...     I.find_customer
    ...     I.check_balance
    ...     I.persist_payment
    ...
    ...     async def find_order(self, state):
    ...         state.order = await self.load_order(state.order_id)
    ...
    ...     async def find_customer(self, state):
    ...         state.customer = await self.load_customer(state.customer_id)
    ...
    ...     async def check_balance(self, state):
    ...         if not state.order.affordable_for(state.customer):
    ...             raise Exception
    ...
    ...     async def persist_payment(self, state):
    ...         state.payment = await self.create_payment(
    ...             order_id=state.order_id, customer_id=state.customer_id
    ...         )
    ...
    ...     load_order: Coroutine
    ...     load_customer: Coroutine
    ...     create_payment: Coroutine

    >>> purchase = Purchase(
    ...     load_order=load_order,
    ...     load_customer=load_customer,
    ...     create_payment=create_payment,
    ... )

    >>> state = SimpleNamespace(order_id=1, customer_id=1)

    >>> asyncio.run(purchase(state))

    ```

<p align="center">&mdash; ⭐ &mdash;</p>
