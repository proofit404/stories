from collections.abc import Callable
from dataclasses import dataclass
from types import SimpleNamespace as State

from app.gateways import send_notification
from app.repositories import charge_money_query
from app.repositories import lock_item_query
from app.transactions import atomic
from stories import I
from stories import Story


@dataclass
class Purchase(Story):
    I.lock_item
    I.charge_money
    I.notify_user

    def lock_item(self, state: State) -> None:
        self.lock_item_query()

    def charge_money(self, state: State) -> None:
        self.charge_money_query()

    def notify_user(self, state: State) -> None:
        self.send_notification(state.user_id)

    lock_item_query: Callable[[], None]
    charge_money_query: Callable[[], None]
    send_notification: Callable[[int], None]


purchase = Purchase(
    lock_item_query=atomic(lock_item_query),
    charge_money_query=atomic(charge_money_query),
    send_notification=send_notification,
)


purchase(State(user_id=1))
