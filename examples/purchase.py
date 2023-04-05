from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from types import SimpleNamespace as State

from app.repositories import create_payment
from app.repositories import load_customer
from app.repositories import load_order

from stories import story


@story
def purchase(it: Steps, state: State) -> None:
    it.find_order(state)
    it.find_customer(state)
    it.check_balance(state)
    it.persist_payment(state)


@dataclass
class Steps:
    load_order: Callable
    load_customer: Callable
    create_payment: Callable

    def find_order(self, state: State) -> None:
        state.order = self.load_order(state.order_id)

    def find_customer(self, state: State) -> None:
        state.customer = self.load_customer(state.customer_id)

    def check_balance(self, state: State) -> None:
        if not state.order.affordable_for(state.customer):
            raise Exception

    def persist_payment(self, state: State) -> None:
        state.payment = self.create_payment(
            order_id=state.order_id, customer_id=state.customer_id
        )


steps = Steps(
    load_order=load_order, load_customer=load_customer, create_payment=create_payment
)


state = State(order_id=1, customer_id=1)


purchase(steps, state)


print(state.payment)
