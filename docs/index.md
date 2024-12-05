# stories

Service objects designed with OOP in mind.

**[PyPI](https://pypi.org/project/stories) |
[Documentation](https://proofit404.github.io/stories) |
[Source Code](https://github.com/proofit404/stories) |
[Task Tracker](https://github.com/proofit404/stories/issues)**

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

>>> state  # doctest: +SKIP

>>> state.payment.was_received()
False

```

## Questions

If you have any questions, feel free to create an issue in our
[Task Tracker](https://github.com/proofit404/stories/issues). We have the
[question label](https://github.com/proofit404/stories/issues?q=is%3Aopen+is%3Aissue+label%3Aquestion)
exactly for this purpose.

## Enterprise support

If you have an issue with any version of the library, you can apply for a paid
enterprise support contract. This will guarantee you that no breaking changes
will happen to you. No matter how old version you're using at the moment. All
necessary features and bug fixes will be backported in a way that serves your
needs.

Please contact [proofit404@gmail.com](mailto:proofit404@gmail.com) if you're
interested in it.

## License

`stories` library is offered under the two clause BSD license.
