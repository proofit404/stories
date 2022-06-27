# State

It's hard to figure out what variables could be set by story. Or what arguments
it does expect as input. It is possible to make this state contract explicit.
You could inherit from `State` class and define allowed variables and arguments
on it.

## Principles

- [Variable allow attribute assignment](#variable-allow-attribute-assignment)
- [Argument allow constructor usage](#argument-allow-constructor-usage)
- [Only declared variables could be assigned](#only-declared-variables-could-be-assigned)
- [Only declared arguments could be passed](#only-declared-arguments-could-be-passed)
- [Attribute assignment validates variable value](#attribute-assignment-validates-variable-value)
- [Constructor argument validates passed value](#constructor-argument-validates-passed-value)
- [Validation errors are propagated as usual errors](#validation-errors-are-propagated-as-usual-errors)
- [Validation errors would be raised by constructor](#validation-errors-would-be-raised-by-constructor)
- [Validation could normalize value](#validation-could-normalize-value)
- [State union joins all defined variables](#state-union-joins-all-defined-variables)

### Variable allow attribute assignment

Classes inherited from `State` could reduce set of variables which allowed to be
defined by attribute assignment. If you declare variable on the state class, it
could be assignment once inside step method.

=== "sync"

    ```pycon

    >>> from dataclasses import dataclass
    >>> from typing import Callable
    >>> from stories import Story, I, State, Variable
    >>> from app.repositories import load_order, load_customer, create_payment

    >>> @dataclass
    ... class Purchase(Story):
    ...     I.find_order
    ...     I.find_customer
    ...     I.check_balance
    ...     I.persist_payment
    ...
    ...     def find_order(self, state):
    ...         state.order = self.load_order(order_id=1)
    ...
    ...     def find_customer(self, state):
    ...         state.customer = self.load_customer(customer_id=1)
    ...
    ...     def check_balance(self, state):
    ...         if not state.order.affordable_for(state.customer):
    ...             raise Exception
    ...
    ...     def persist_payment(self, state):
    ...         state.payment = self.create_payment(order_id=1, customer_id=1)
    ...
    ...     load_order: Callable
    ...     load_customer: Callable
    ...     create_payment: Callable

    >>> class PurchaseState(State):
    ...     order = Variable()
    ...     customer = Variable()
    ...     payment = Variable()

    >>> purchase = Purchase(
    ...     load_order=load_order,
    ...     load_customer=load_customer,
    ...     create_payment=create_payment,
    ... )

    >>> state = PurchaseState()

    >>> purchase(state)

    >>> state.payment
    Payment(due_date=datetime.datetime(1999, 12, 31, 0, 0))

    ```

=== "async"

    ```pycon

    >>> import asyncio
    >>> from dataclasses import dataclass
    >>> from typing import Coroutine
    >>> from stories import Story, I, State, Variable
    >>> from aioapp.repositories import load_order, load_customer, create_payment

    >>> @dataclass
    ... class Purchase(Story):
    ...     I.find_order
    ...     I.find_customer
    ...     I.check_balance
    ...     I.persist_payment
    ...
    ...     async def find_order(self, state):
    ...         state.order = await self.load_order(order_id=1)
    ...
    ...     async def find_customer(self, state):
    ...         state.customer = await self.load_customer(customer_id=1)
    ...
    ...     async def check_balance(self, state):
    ...         if not state.order.affordable_for(state.customer):
    ...             raise Exception
    ...
    ...     async def persist_payment(self, state):
    ...         state.payment = await self.create_payment(
    ...             order_id=1, customer_id=1
    ...         )
    ...
    ...     load_order: Coroutine
    ...     load_customer: Coroutine
    ...     create_payment: Coroutine

    >>> class PurchaseState(State):
    ...     order = Variable()
    ...     customer = Variable()
    ...     payment = Variable()

    >>> purchase = Purchase(
    ...     load_order=load_order,
    ...     load_customer=load_customer,
    ...     create_payment=create_payment,
    ... )

    >>> state = PurchaseState()

    >>> asyncio.run(purchase(state))

    >>> state.payment
    Payment(due_date=datetime.datetime(1999, 12, 31, 0, 0))

    ```

### Argument allow constructor usage

Argument declaration is superset of the Variable declaration. All rules applied
to Variable applies to Argument as well. For example, variable declared as
Argument is allowed to be assigned as attribute by one of the story step.

However, Argument declaration allows variable with that name to be passed to the
state constructor before story execution would even starts.

=== "sync"

    ```pycon

    >>> from dataclasses import dataclass
    >>> from typing import Callable
    >>> from stories import Story, I, State, Argument, Variable
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

    >>> class PurchaseState(State):
    ...     order_id = Argument()
    ...     customer_id = Argument()
    ...     order = Variable()
    ...     customer = Variable()
    ...     payment = Variable()

    >>> purchase = Purchase(
    ...     load_order=load_order,
    ...     load_customer=load_customer,
    ...     create_payment=create_payment,
    ... )

    >>> state = PurchaseState(order_id=1, customer_id=1)

    >>> purchase(state)

    >>> state.payment
    Payment(due_date=datetime.datetime(1999, 12, 31, 0, 0))

    ```

=== "async"

    ```pycon

    >>> import asyncio
    >>> from dataclasses import dataclass
    >>> from typing import Coroutine
    >>> from stories import Story, I, State, Argument, Variable
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

    >>> class PurchaseState(State):
    ...     order_id = Argument()
    ...     customer_id = Argument()
    ...     order = Variable()
    ...     customer = Variable()
    ...     payment = Variable()

    >>> purchase = Purchase(
    ...     load_order=load_order,
    ...     load_customer=load_customer,
    ...     create_payment=create_payment,
    ... )

    >>> state = PurchaseState(order_id=1, customer_id=1)

    >>> asyncio.run(purchase(state))

    >>> state.payment
    Payment(due_date=datetime.datetime(1999, 12, 31, 0, 0))

    ```

### Only declared variables could be assigned

Variables with random names allowed to be assigned only if you would use plain
`State` object. If you declare variables using inheritance from `State` class,
only declared variables would be allowed to be assigned later by steps. If you
try to assing unknown variable, an error would be raised.

=== "sync"

    ```pycon

    >>> from dataclasses import dataclass
    >>> from typing import Callable
    >>> from stories import Story, I, State, Variable
    >>> from app.repositories import load_order

    >>> @dataclass
    ... class Purchase(Story):
    ...     I.find_order
    ...
    ...     def find_order(self, state):
    ...         state.order = self.load_order(order_id=1)
    ...
    ...     load_order: Callable

    >>> class PurchaseState(State):
    ...     customer = Variable()

    >>> purchase = Purchase(load_order=load_order)

    >>> state = PurchaseState()

    >>> purchase(state)
    Traceback (most recent call last):
      ...
    _stories.exceptions.StateError: Unknown variable assignment: order
    <BLANKLINE>
    PurchaseState

    ```

=== "async"

    ```pycon

    >>> import asyncio
    >>> from dataclasses import dataclass
    >>> from typing import Coroutine
    >>> from stories import Story, I, State, Variable
    >>> from aioapp.repositories import load_order

    >>> @dataclass
    ... class Purchase(Story):
    ...     I.find_order
    ...
    ...     async def find_order(self, state):
    ...         state.order = await self.load_order(order_id=1)
    ...
    ...     load_order: Coroutine

    >>> class PurchaseState(State):
    ...     customer = Variable()

    >>> purchase = Purchase(load_order=load_order)

    >>> state = PurchaseState()

    >>> asyncio.run(purchase(state))
    Traceback (most recent call last):
      ...
    _stories.exceptions.StateError: Unknown variable assignment: order
    <BLANKLINE>
    PurchaseState

    ```

### Only declared arguments could be passed

If you try to pass an argument to the state class which was not declared using
`Argument`, error would be thrown immediately. Even if you declare state
attribute using `Variable` it will not be allowed to be used as state
constructor argument.

=== "sync"

    ```pycon

    >>> from dataclasses import dataclass
    >>> from typing import Callable
    >>> from stories import Story, I, State, Argument, Variable
    >>> from app.repositories import load_order

    >>> @dataclass
    ... class Purchase(Story):
    ...     I.find_order
    ...
    ...     def find_order(self, state):
    ...         state.order = self.load_order(state.order_id)
    ...
    ...     load_order: Callable

    >>> class PurchaseState(State):
    ...     order_id = Argument()
    ...     order = Variable()

    >>> purchase = Purchase(load_order=load_order)

    >>> PurchaseState(customer_id=1)
    Traceback (most recent call last):
      ...
    _stories.exceptions.StateError: Unknown argument passed: customer_id
    <BLANKLINE>
    PurchaseState

    ```

=== "async"

    ```pycon

    >>> import asyncio
    >>> from dataclasses import dataclass
    >>> from typing import Coroutine
    >>> from stories import Story, I, State, Argument, Variable
    >>> from aioapp.repositories import load_order

    >>> @dataclass
    ... class Purchase(Story):
    ...     I.find_order
    ...
    ...     async def find_order(self, state):
    ...         state.order = await self.load_order(state.order_id)
    ...
    ...     load_order: Coroutine

    >>> class PurchaseState(State):
    ...     order_id = Argument()
    ...     order = Variable()

    >>> purchase = Purchase(load_order=load_order)

    >>> PurchaseState(customer_id=1)
    Traceback (most recent call last):
      ...
    _stories.exceptions.StateError: Unknown argument passed: customer_id
    <BLANKLINE>
    PurchaseState

    ```

### Attribute assignment validates variable value

When story step assign attributes to the state, validator passed to the
`Variable` would be applied to the value.

Validator is a function of single argument. It should return attribute value or
raise exception if value is wrong.

If validator returns a value, it will be assigned to the state attribute.

=== "sync"

    ```pycon

    >>> from dataclasses import dataclass
    >>> from typing import Callable
    >>> from stories import Story, I, State, Variable
    >>> from app.repositories import load_order
    >>> from app.entities import Order

    >>> def is_order(value):
    ...     if isinstance(value, Order):
    ...         return value
    ...     else:
    ...         raise Exception(f"{value!r} is not valid order")

    >>> @dataclass
    ... class Purchase(Story):
    ...     I.find_order
    ...
    ...     def find_order(self, state):
    ...         state.order = self.load_order(order_id=1)
    ...
    ...     load_order: Callable

    >>> class PurchaseState(State):
    ...     order = Variable(is_order)

    >>> purchase = Purchase(load_order=load_order)

    >>> state = PurchaseState()

    >>> purchase(state)

    >>> state.order
    Order(product=Product(name='Books'), cost=Cost(at=datetime.datetime(1999, 12, 31, 0, 0), amount=7))

    ```

=== "async"

    ```pycon

    >>> import asyncio
    >>> from dataclasses import dataclass
    >>> from typing import Coroutine
    >>> from stories import Story, I, State, Variable
    >>> from aioapp.repositories import load_order
    >>> from aioapp.entities import Order

    >>> def is_order(value):
    ...     if isinstance(value, Order):
    ...         return value
    ...     else:
    ...         raise Exception(f'{value!r} is not valid order')

    >>> @dataclass
    ... class Purchase(Story):
    ...     I.find_order
    ...
    ...     async def find_order(self, state):
    ...         state.order = await self.load_order(order_id=1)
    ...
    ...     load_order: Coroutine

    >>> class PurchaseState(State):
    ...     order = Variable(is_order)

    >>> purchase = Purchase(load_order=load_order)

    >>> state = PurchaseState()

    >>> asyncio.run(purchase(state))

    >>> state.order
    Order(product=Product(name='Books'), cost=Cost(at=datetime.datetime(1999, 12, 31, 0, 0), amount=7))

    ```

### Constructor argument validates passed value

When pass arguments to the state constructor, validator passed to the `Argument`
would be applied to the value.

Validator is a function of single argument. It should return argument value or
raise exception if value is wrong.

If validator returns a value, it will be assigned to the state attribute.

=== "sync"

    ```pycon

    >>> from dataclasses import dataclass
    >>> from typing import Callable
    >>> from stories import Story, I, State, Argument
    >>> from app.repositories import load_order
    >>> from app.entities import Order

    >>> def is_order_id(value):
    ...     if isinstance(value, int):
    ...         return value
    ...     else:
    ...         raise Exception(f"{value!r} is not valid order id")

    >>> def is_order(value):
    ...     if isinstance(value, Order):
    ...         return value
    ...     else:
    ...         raise Exception(f"{value!r} is not valid order")

    >>> @dataclass
    ... class Purchase(Story):
    ...     I.find_order
    ...
    ...     def find_order(self, state):
    ...         state.order = self.load_order(state.order_id)
    ...
    ...     load_order: Callable

    >>> class PurchaseState(State):
    ...     order_id = Argument(is_order_id)
    ...     order = Variable(is_order)

    >>> purchase = Purchase(load_order=load_order)

    >>> state = PurchaseState(order_id=1)

    >>> purchase(state)

    >>> state.order_id
    1

    ```

=== "async"

    ```pycon

    >>> import asyncio
    >>> from dataclasses import dataclass
    >>> from typing import Coroutine
    >>> from stories import Story, I, State, Argument
    >>> from aioapp.repositories import load_order
    >>> from aioapp.entities import Order

    >>> def is_order_id(value):
    ...     if isinstance(value, int):
    ...         return value
    ...     else:
    ...         raise Exception(f'{value!r} is not valid order id')

    >>> def is_order(value):
    ...     if isinstance(value, Order):
    ...         return value
    ...     else:
    ...         raise Exception(f'{value!r} is not valid order')

    >>> @dataclass
    ... class Purchase(Story):
    ...     I.find_order
    ...
    ...     async def find_order(self, state):
    ...         state.order = await self.load_order(state.order_id)
    ...
    ...     load_order: Coroutine

    >>> class PurchaseState(State):
    ...     order_id = Argument(is_order_id)
    ...     order = Variable(is_order)

    >>> purchase = Purchase(load_order=load_order)

    >>> state = PurchaseState(order_id=1)

    >>> asyncio.run(purchase(state))

    >>> state.order_id
    1

    ```

### Validation errors are propagated as usual errors

If validation function raises exception, story execution would stops. It would
be propagated as usual exception which could happend inside the step.

=== "sync"

    ```pycon

    >>> from dataclasses import dataclass
    >>> from typing import Callable
    >>> from stories import Story, I, State, Variable

    >>> @dataclass
    ... class Purchase(Story):
    ...     I.find_order
    ...
    ...     def find_order(self, state):
    ...         state.order = self.load_order(order_id=1)
    ...
    ...     load_order: Callable

    >>> class PurchaseState(State):
    ...     order = Variable(is_order)

    >>> purchase = Purchase(load_order=lambda order_id: None)

    >>> state = PurchaseState()

    >>> purchase(state)
    Traceback (most recent call last):
      ...
    Exception: None is not valid order

    ```

=== "async"

    ```pycon

    >>> import asyncio
    >>> from dataclasses import dataclass
    >>> from typing import Coroutine
    >>> from stories import Story, I, State, Variable

    >>> @dataclass
    ... class Purchase(Story):
    ...     I.find_order
    ...
    ...     async def find_order(self, state):
    ...         state.order = await self.load_order(order_id=1)
    ...
    ...     load_order: Coroutine

    >>> class PurchaseState(State):
    ...     order = Variable(is_order)

    >>> async def load_order(order_id):
    ...     pass

    >>> purchase = Purchase(load_order=load_order)

    >>> state = PurchaseState()

    >>> asyncio.run(purchase(state))
    Traceback (most recent call last):
      ...
    Exception: None is not valid order

    ```

### Validation errors would be raised by constructor

If validation funcution raises exception, state constructor would propagate this
error.

=== "sync"

    ```pycon

    >>> from dataclasses import dataclass
    >>> from typing import Callable
    >>> from stories import Story, I, State, Argument
    >>> from app.repositories import load_order

    >>> def is_order_id(value):
    ...     if isinstance(value, int):
    ...         return value
    ...     else:
    ...         raise Exception(f"{value!r} is not valid order id")

    >>> @dataclass
    ... class Purchase(Story):
    ...     I.find_order
    ...
    ...     def find_order(self, state):
    ...         state.order = self.load_order(state.order_id)
    ...
    ...     load_order: Callable

    >>> class PurchaseState(State):
    ...     order_id = Argument(is_order_id)

    >>> purchase = Purchase(load_order=load_order)

    >>> PurchaseState(order_id='1')
    Traceback (most recent call last):
      ...
    Exception: '1' is not valid order id

    ```

=== "async"

    ```pycon

    >>> from dataclasses import dataclass
    >>> from typing import Coroutine
    >>> from stories import Story, I, State, Argument
    >>> from aioapp.repositories import load_order

    >>> def is_order_id(value):
    ...     if isinstance(value, int):
    ...         return value
    ...     else:
    ...         raise Exception(f'{value!r} is not valid order id')

    >>> @dataclass
    ... class Purchase(Story):
    ...     I.find_order
    ...
    ...     async def find_order(self, state):
    ...         state.order = await self.load_order(state.order_id)
    ...
    ...     load_order: Coroutine

    >>> class PurchaseState(State):
    ...     order_id = Argument(is_order_id)

    >>> purchase = Purchase(load_order=load_order)

    >>> PurchaseState(order_id='1')
    Traceback (most recent call last):
      ...
    Exception: '1' is not valid order id

    ```

### Validation could normalize value

Validator function could cast value passed to it to the new type. It's a similar
process to normalization common to API schema libraries. To convert passed value
to something new, just return new thing. New value returned by validator
function would be assigned to the state attribute.

This works both for `Variable` and `Argument` validators.

=== "sync"

    ```pycon

    >>> from dataclasses import dataclass
    >>> from typing import Callable
    >>> from stories import Story, I, State
    >>> from app.entities import Customer

    >>> def is_customer(value):
    ...     if isinstance(value, dict) and value.keys() == {'balance'} and isinstance(value['balance'], int):
    ...         return Customer(value['balance'])
    ...     else:
    ...         raise Exception(f'{value!r} is not valid customer')

    >>> @dataclass
    ... class Purchase(Story):
    ...     I.find_customer
    ...
    ...     def find_customer(self, state):
    ...         state.customer = self.load_customer(customer_id=1)
    ...
    ...     load_customer: Callable

    >>> class PurchaseState(State):
    ...     customer = Variable(is_customer)

    >>> def load_customer(customer_id):
    ...     return {'balance': 100}

    >>> purchase = Purchase(load_customer=load_customer)

    >>> state = PurchaseState()

    >>> purchase(state)

    >>> state.customer
    Customer(balance=100)

    ```

=== "async"

    ```pycon

    >>> import asyncio
    >>> from dataclasses import dataclass
    >>> from typing import Coroutine
    >>> from stories import Story, I, State, Variable
    >>> from app.entities import Customer

    >>> def is_customer(value):
    ...     if isinstance(value, dict) and value.keys() == {'balance'} and isinstance(value['balance'], int):
    ...         return Customer(value['balance'])
    ...     else:
    ...         raise Exception(f'{value!r} is not valid customer')

    >>> @dataclass
    ... class Purchase(Story):
    ...     I.find_customer
    ...
    ...     async def find_customer(self, state):
    ...         state.customer = await self.load_customer(customer_id=1)
    ...
    ...     load_customer: Coroutine

    >>> class PurchaseState(State):
    ...     customer = Variable(is_customer)

    >>> async def load_customer(customer_id):
    ...     return {'balance': 100}

    >>> purchase = Purchase(load_customer=load_customer)

    >>> state = PurchaseState()

    >>> asyncio.run(purchase(state))

    >>> state.customer
    Customer(balance=100)

    ```

### State union joins all defined variables

Story composition requires complicated state object which would define variables
necessary for both stories. If you defined separate state classes for both
stories, you could join variables with `State` union operation.

State union would include all variables defined in separate State classes.

=== "sync"

    ```pycon

    >>> from dataclasses import dataclass
    >>> from typing import Callable
    >>> from stories import Story, I, State, Variable
    >>> from app.repositories import load_order, load_customer, create_payment
    >>> from app.entities import Order, Customer, Payment

    >>> def is_order(value):
    ...     assert isinstance(value, Order)
    ...     return value

    >>> def is_customer(value):
    ...     assert isinstance(value, Customer)
    ...     return value

    >>> def is_payment(value):
    ...     assert isinstance(value, Payment)
    ...     return value

    >>> @dataclass
    ... class Purchase(Story):
    ...     I.find_order
    ...     I.find_customer
    ...     I.pay
    ...
    ...     def find_order(self, state):
    ...         state.order = self.load_order(order_id=1)
    ...
    ...     def find_customer(self, state):
    ...         state.customer = self.load_customer(customer_id=1)
    ...
    ...     load_order: Callable
    ...     load_customer: Callable
    ...     pay: Story

    >>> class PurchaseState(State):
    ...     order = Variable(is_order)
    ...     customer = Variable(is_customer)

    >>> @dataclass
    ... class Pay(Story):
    ...     I.persist_payment
    ...
    ...     def persist_payment(self, state):
    ...         state.payment = self.create_payment(
    ...             order_id=1, customer_id=1
    ...         )
    ...
    ...     create_payment: Callable

    >>> class PayState(State):
    ...     payment = Variable(is_payment)

    >>> pay = Pay(create_payment=create_payment)

    >>> purchase = Purchase(
    ...     load_order=load_order,
    ...     load_customer=load_customer,
    ...     pay=pay,
    ... )

    >>> state_class = PurchaseState & PayState

    >>> state = state_class()

    >>> purchase(state)

    >>> state.payment
    Payment(due_date=datetime.datetime(1999, 12, 31, 0, 0))

    ```

=== "async"

    ```pycon

    >>> import asyncio
    >>> from dataclasses import dataclass
    >>> from typing import Coroutine
    >>> from stories import Story, I, State, Variable
    >>> from aioapp.repositories import load_order, load_customer, create_payment
    >>> from aioapp.entities import Order, Customer, Payment

    >>> def is_order(value):
    ...     assert isinstance(value, Order)
    ...     return value

    >>> def is_customer(value):
    ...     assert isinstance(value, Customer)
    ...     return value

    >>> def is_payment(value):
    ...     assert isinstance(value, Payment)
    ...     return value

    >>> @dataclass
    ... class Purchase(Story):
    ...     I.find_order
    ...     I.find_customer
    ...     I.pay
    ...
    ...     async def find_order(self, state):
    ...         state.order = await self.load_order(order_id=1)
    ...
    ...     async def find_customer(self, state):
    ...         state.customer = await self.load_customer(customer_id=1)
    ...
    ...     load_order: Callable
    ...     load_customer: Callable
    ...     pay: Story

    >>> @dataclass
    ... class Pay(Story):
    ...     I.persist_payment
    ...
    ...     async def persist_payment(self, state):
    ...         state.payment = await self.create_payment(
    ...             order_id=1, customer_id=1
    ...         )
    ...
    ...     create_payment: Callable

    >>> class PurchaseState(State):
    ...     order = Variable(is_order)
    ...     customer = Variable(is_customer)

    >>> class PayState(State):
    ...     payment = Variable(is_payment)

    >>> pay = Pay(create_payment=create_payment)

    >>> purchase = Purchase(
    ...     load_order=load_order,
    ...     load_customer=load_customer,
    ...     pay=pay,
    ... )

    >>> state_class = PurchaseState & PayState

    >>> state = state_class()

    >>> asyncio.run(purchase(state))

    >>> state.payment
    Payment(due_date=datetime.datetime(1999, 12, 31, 0, 0))

    ```

<p align="center">&mdash; ⭐ &mdash;</p>
