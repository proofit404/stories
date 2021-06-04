# Transaction management

It's possible to handle database transactions in different ways inside stories.

## Single steps

If you need to wrap single story step in a database transaction, don't do that
inside the step itself. Stories you write should not be aware of the database
you use.

Ideally, stories are written with composition in mind. You'll be able to
decorate injected function in the construction process.

```pycon

>>> from dataclasses import dataclass
>>> from typing import Callable
>>> from stories import Story, I, State

>>> @dataclass
... class Purchase(Story):
...     I.lock_item
...     I.charge_money
...     I.notify_user
...
...     def lock_item(self, state):
...         self.lock_item_query()
...
...     def charge_money(self, state):
...         self.charge_money_query()
...
...     def notify_user(self, state):
...         self.send_notification(state.user_id)
...
...     lock_item_query: Callable
...     charge_money_query: Callable
...     send_notification: Callable

```

You don't need to wrap with transaction the step itself. It's better to wrap
with transaction an injected functions.

```pycon

>>> from app.transactions import atomic
>>> from app.repositories import lock_item_query, charge_money_query
>>> from app.gateways import send_notification

>>> purchase = Purchase(
...     lock_item_query=atomic(lock_item_query),
...     charge_money_query=atomic(charge_money_query),
...     send_notification=send_notification,
... )

>>> purchase(State(user_id=1))
BEGIN TRANSACTION;
UPDATE 'items';
COMMIT TRANSACTION;
BEGIN TRANSACTION;
UPDATE 'balance';
COMMIT TRANSACTION;

```

## Whole story

If you want to wrap the whole story in a single transaction, don't write special
steps in the beginning and end of the story.

We suggest to have single story with start and end of the transaction. This
story would be able to decorate any story. Rollback will be handled at the same
infrastructure level that compose decorated story.

```pycon

>>> from app.transactions import start_transaction, end_transaction, cancel_transaction

>>> class Persistence:
...
...     def __init__(self):
...         self.started = False
...         self.committed = False
...
...     def start_transaction(self):
...         self.started = True
...         start_transaction()
...
...     def end_transaction(self):
...         self.committed = True
...         end_transaction()
...
...     def finalize(self):
...         if self.started and not self.committed:
...             cancel_transaction()

>>> @dataclass
... class Transactional(Story):
...     I.begin
...     I.wrapped
...     I.end
...
...     def begin(self, state):
...         self.start_transaction()
...
...     def end(self, state):
...         self.end_transaction()
...
...     start_transaction: Callable
...     wrapped: Story
...     end_transaction: Callable

>>> persistence = Persistence()

>>> purchase = Purchase(
...     lock_item_query=lock_item_query,
...     charge_money_query=charge_money_query,
...     send_notification=send_notification,
... )

>>> transactional = Transactional(
...     persistence.start_transaction,
...     purchase,
...     persistence.end_transaction,
... )

>>> try:
...     transactional(State(user_id=1))
... finally:
...     persistence.finalize()
BEGIN TRANSACTION;
UPDATE 'items';
UPDATE 'balance';
COMMIT TRANSACTION;

```

You would see transaction rolling back if nested story fails in the middle of
its execution.

!!! note

    As you may notice, `Persistence` is a stateful object. You need to
    create a dedicated instance of the story for each call! If you
    don't like such behavior consider to redesign `Persistence` class
    to store its flags in the `State` object.

```pycon

>>> from app.tools import log

>>> persistence = Persistence()

>>> transactional = Transactional(
...     persistence.start_transaction,
...     purchase,
...     persistence.end_transaction,
... )

>>> try:
...     transactional(State(user_id=2))
... except Exception:
...     log("ERROR")
... finally:
...     persistence.finalize()
BEGIN TRANSACTION;
UPDATE 'items';
UPDATE 'balance';
ERROR
ROLLBACK TRANSACTION;

```

<p align="center">&mdash; ⭐ &mdash;</p>
<p align="center"><i>The <code>stories</code> library is part of the SOLID python family.</i></p>
