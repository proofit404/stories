# Story

## Principles

- [Story is a callable object](#story-is-a-callable-object)
- [Steps executed in specified order](#steps-executed-in-specified-order)
- [Steps could assign state variables](#steps-could-assign-state-variables)
- [Story state would be available after its execution](#story-state-would-be-available-after-its-execution)
- [Exceptions would be propagated](#exceptions-would-be-propagated)

### Story is a callable object

Story is an object which you should call if you want to execute story steps.
When you inherit from `Story` class, you basically define `__call__` and
`__repr__` methods on the class you own. It is nothing more than that under the
hood.

As you may notice, we don't require any specific way to instantiate the class.
It's up to you whether or not to use libraries like `attrs`, `dataclasses`,
`pydantic` or use plain `__init__` method instead.

=== "attrs"

    ```pycon

    >>> from typing import Callable
    >>> from attr import attrs, attrib
    >>> from stories import Story, I

    >>> @attrs
    ... class Purchase(Story):
    ...     I.find_order
    ...     I.find_customer
    ...     I.persist_payment
    ...
    ...     def find_order(self, state):
    ...         state.order = self.load_order(state.order_id)
    ...
    ...     def find_customer(self, state):
    ...         state.customer = self.load_customer(state.customer_id)
    ...
    ...     def persist_payment(self, state):
    ...         self.create_payment(state.order_id, state.customer_id)
    ...
    ...     load_order = attrib()
    ...     load_customer = attrib()
    ...     create_payment = attrib()

    ```

=== "dataclasses"

    ```pycon

    >>> from dataclasses import dataclass
    >>> from typing import Callable
    >>> from stories import Story, I

    >>> @dataclass
    ... class Purchase(Story):
    ...     I.find_order
    ...     I.find_customer
    ...     I.persist_payment
    ...
    ...     def find_order(self, state):
    ...         state.order = self.load_order(state.order_id)
    ...
    ...     def find_customer(self, state):
    ...         state.customer = self.load_customer(state.customer_id)
    ...
    ...     def persist_payment(self, state):
    ...         self.create_payment(state.order_id, state.customer_id)
    ...
    ...     load_order: Callable
    ...     load_customer: Callable
    ...     create_payment: Callable

    ```

=== "pydantic"

    ```pycon

    >>> from typing import Callable
    >>> from pydantic.dataclasses import dataclass
    >>> from stories import Story, I

    >>> @dataclass
    ... class Purchase(Story):
    ...     I.find_order
    ...     I.find_customer
    ...     I.persist_payment
    ...
    ...     def find_order(self, state):
    ...         state.order = self.load_order(state.order_id)
    ...
    ...     def find_customer(self, state):
    ...         state.customer = self.load_customer(state.customer_id)
    ...
    ...     def persist_payment(self, state):
    ...         self.create_payment(state.order_id, state.customer_id)
    ...
    ...     load_order: Callable
    ...     load_customer: Callable
    ...     create_payment: Callable

    ```

=== "`__init__`"

    ```pycon

    >>> from stories import Story, I

    >>> class Purchase(Story):
    ...     I.find_order
    ...     I.find_customer
    ...     I.persist_payment
    ...
    ...     def find_order(self, state):
    ...         state.order = self.load_order(state.order_id)
    ...
    ...     def find_customer(self, state):
    ...         state.customer = self.load_customer(state.customer_id)
    ...
    ...     def persist_payment(self, state):
    ...         self.create_payment(state.order_id, state.customer_id)
    ...
    ...     def __init__(self, load_order, load_customer, create_payment):
    ...         self.load_order = load_order
    ...         self.load_customer = load_customer
    ...         self.create_payment = create_payment

    ```

### Steps executed in specified order

To call the story, you need to instantiate the class first. After that you could
pass `State` object to the story call and story would be executed.

If methods of the story are coroutines, you need to `await` story call as well.
The same as you do with regular coroutine methods defined on your classes.

=== "sync"

    ```pycon

    >>> from dataclasses import dataclass
    >>> from typing import Callable
    >>> from stories import Story, I, State
    >>> from app.repositories import load_order, load_customer, create_payment
    >>> from app.tools import log

    >>> @dataclass
    ... class Purchase(Story):
    ...     I.find_order
    ...     I.find_customer
    ...     I.check_balance
    ...     I.persist_payment
    ...
    ...     def find_order(self, state):
    ...         self.log("==> find order")
    ...         state.order = self.load_order(state.order_id)
    ...
    ...     def find_customer(self, state):
    ...         self.log("==> find customer")
    ...         state.customer = self.load_customer(state.customer_id)
    ...
    ...     def check_balance(self, state):
    ...         self.log("==> check balance")
    ...         if not state.order.affordable_for(state.customer):
    ...             raise Exception
    ...
    ...     def persist_payment(self, state):
    ...         self.log("==> persist payment")
    ...         state.payment = self.create_payment(
    ...             order_id=state.order_id, customer_id=state.customer_id
    ...         )
    ...
    ...     log: Callable
    ...     load_order: Callable
    ...     load_customer: Callable
    ...     create_payment: Callable

    >>> purchase = Purchase(
    ...     log=log,
    ...     load_order=load_order,
    ...     load_customer=load_customer,
    ...     create_payment=create_payment,
    ... )

    >>> state = State(order_id=1, customer_id=1)

    >>> purchase(state)
    ==> find order
    ==> find customer
    ==> check balance
    ==> persist payment

    ```

=== "async"

    ```pycon

    >>> import asyncio
    >>> from dataclasses import dataclass
    >>> from typing import Coroutine
    >>> from stories import Story, I, State
    >>> from aioapp.repositories import load_order, load_customer, create_payment
    >>> from aioapp.tools import log

    >>> @dataclass
    ... class Purchase(Story):
    ...     I.find_order
    ...     I.find_customer
    ...     I.check_balance
    ...     I.persist_payment
    ...
    ...     async def find_order(self, state):
    ...         await self.log("==> find order")
    ...         state.order = await self.load_order(state.order_id)
    ...
    ...     async def find_customer(self, state):
    ...         await self.log("==> find customer")
    ...         state.customer = await self.load_customer(state.customer_id)
    ...
    ...     async def check_balance(self, state):
    ...         await self.log("==> check balance")
    ...         if not state.order.affordable_for(state.customer):
    ...             raise Exception
    ...
    ...     async def persist_payment(self, state):
    ...         await self.log("==> persist payment")
    ...         state.payment = await self.create_payment(
    ...             order_id=state.order_id, customer_id=state.customer_id
    ...         )
    ...
    ...     log: Coroutine
    ...     load_order: Coroutine
    ...     load_customer: Coroutine
    ...     create_payment: Coroutine

    >>> purchase = Purchase(
    ...     log=log,
    ...     load_order=load_order,
    ...     load_customer=load_customer,
    ...     create_payment=create_payment,
    ... )

    >>> state = State(order_id=1, customer_id=1)

    >>> asyncio.run(purchase(state))
    ==> find order
    ==> find customer
    ==> check balance
    ==> persist payment

    ```

### Steps could assign state variables

Every step could assign variable in state object. Story steps executed
afterwards would be able to access variables assigned earlier. If you use plain
`State` object, you could use any variable names. No restrictions applied to
allowed name of the variable or its value.

As you could see in the example below, the `check_balance` step is able to
access `order` and `customer` variables set by previous steps.

=== "sync"

    ```pycon

    >>> from dataclasses import dataclass
    >>> from typing import Callable
    >>> from stories import Story, I, State
    >>> from app.repositories import load_order, load_customer, create_payment

    >>> @dataclass
    ... class Purchase(Story):
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

    >>> state = State(order_id=1, customer_id=1)

    >>> purchase(state)

    ```

=== "async"

    ```pycon

    >>> import asyncio
    >>> from dataclasses import dataclass
    >>> from typing import Coroutine
    >>> from stories import Story, I, State
    >>> from aioapp.repositories import load_order, load_customer, create_payment

    >>> @dataclass
    ... class Purchase(Story):
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

    >>> state = State(order_id=1, customer_id=1)

    >>> asyncio.run(purchase(state))

    ```

### Story state would be available after its execution

After story execution all state variables would be available in the same state
object you have passed to it.

You would be able to access same objects that were assigned by story steps.

=== "sync"

    ```pycon

    >>> from dataclasses import dataclass
    >>> from typing import Callable
    >>> from stories import Story, I, State
    >>> from app.repositories import load_order, load_customer, create_payment

    >>> @dataclass
    ... class Purchase(Story):
    ...     I.find_order
    ...     I.find_customer
    ...     I.persist_payment
    ...
    ...     def find_order(self, state):
    ...         state.order = self.load_order(state.order_id)
    ...
    ...     def find_customer(self, state):
    ...         state.customer = self.load_customer(state.customer_id)
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

    >>> state = State(order_id=1, customer_id=1)

    >>> purchase(state)

    >>> state.order
    Order(product=Product(name='Books'), cost=Cost(at=datetime.datetime(1999, 12, 31, 0, 0), amount=7))

    >>> state.order.product
    Product(name='Books')

    >>> state.customer
    Customer(balance=8)

    >>> state.payment
    Payment(due_date=datetime.datetime(1999, 12, 31, 0, 0))

    ```

=== "async"

    ```pycon

    >>> import asyncio
    >>> from dataclasses import dataclass
    >>> from typing import Coroutine
    >>> from stories import Story, I, State
    >>> from aioapp.repositories import load_order, load_customer, create_payment

    >>> @dataclass
    ... class Purchase(Story):
    ...     I.find_order
    ...     I.find_customer
    ...     I.persist_payment
    ...
    ...     async def find_order(self, state):
    ...         state.order = await self.load_order(state.order_id)
    ...
    ...     async def find_customer(self, state):
    ...         state.customer = await self.load_customer(state.customer_id)
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

    >>> state = State(order_id=1, customer_id=1)

    >>> asyncio.run(purchase(state))

    >>> state.order
    Order(product=Product(name='Books'), cost=Cost(at=datetime.datetime(1999, 12, 31, 0, 0), amount=7))

    >>> state.order.product
    Product(name='Books')

    >>> state.customer
    Customer(balance=8)

    >>> state.payment
    Payment(due_date=datetime.datetime(1999, 12, 31, 0, 0))

    ```

### Exceptions would be propagated

If exception was raised inside the step method, execution of the story would
stop at that moment and exception would be raised to the caller code without any
changes.

=== "sync"

    ```pycon

    >>> from dataclasses import dataclass
    >>> from typing import Callable
    >>> from stories import Story, I, State
    >>> from app.tools import log

    >>> @dataclass
    ... class Purchase(Story):
    ...     I.find_order
    ...     I.find_customer
    ...     I.check_balance
    ...     I.persist_payment
    ...
    ...     def find_order(self, state):
    ...         self.log("==> find order")
    ...
    ...     def find_customer(self, state):
    ...         self.log("==> find customer")
    ...
    ...     def check_balance(self, state):
    ...         self.log("==> check balance")
    ...         raise Exception("Not enough money")
    ...
    ...     def persist_payment(self, state):
    ...         self.log("==> persist payment")
    ...
    ...     log: Callable

    >>> purchase = Purchase(log=log)

    >>> state = State()

    >>> try:
    ...     purchase(state)
    ... except Exception as error:
    ...     print(f"==> {error!r}")
    ==> find order
    ==> find customer
    ==> check balance
    ==> Exception('Not enough money')

    ```

=== "async"

    ```pycon

    >>> import asyncio
    >>> from dataclasses import dataclass
    >>> from typing import Coroutine
    >>> from stories import Story, I, State
    >>> from aioapp.tools import log

    >>> @dataclass
    ... class Purchase(Story):
    ...     I.find_order
    ...     I.find_customer
    ...     I.check_balance
    ...     I.persist_payment
    ...
    ...     async def find_order(self, state):
    ...         await self.log("==> find order")
    ...
    ...     async def find_customer(self, state):
    ...         await self.log("==> find customer")
    ...
    ...     async def check_balance(self, state):
    ...         await self.log("==> check balance")
    ...         raise Exception("Not enough money")
    ...
    ...     async def persist_payment(self, state):
    ...         await self.log("==> persist payment")
    ...
    ...     log: Coroutine

    >>> purchase = Purchase(log=log)

    >>> state = State()

    >>> try:
    ...     asyncio.run(purchase(state))
    ... except Exception as error:
    ...     print(f"==> {error!r}")
    ==> find order
    ==> find customer
    ==> check balance
    ==> Exception('Not enough money')

    ```

<p align="center">&mdash; ⭐ &mdash;</p>
<p align="center"><i>The <code>stories</code> library is part of the SOLID python family.</i></p>
