from __future__ import annotations

from collections.abc import Callable
from typing import NewType

from pydantic import Field
from pydantic.dataclasses import dataclass

from app.entities import Customer
from app.entities import Order
from app.entities import Payment


@dataclass
class Purchase:
    def find_order(self, state: State) -> None:
        state.order = self.load_order(state.order_id)

    def find_customer(self, state: State) -> None:
        state.customer = self.load_customer(state.customer_id)

    def check_balance(self, state: State) -> None:
        if not state.order.affordable_for(state.customer):
            raise LowFunds()

    def persist_payment(self, state: State) -> None:
        state.payment = self.create_payment(state.customer_id, state.order_id)

    load_order: Callable[[OrderId], Order]
    load_customer: Callable[[CustomerId], Customer]
    create_payment: Callable[[CustomerId, OrderId], Payment]


OrderId = NewType("OrderId", int)


CustomerId = NewType("CustomerId", int)


@dataclass(config={"validate_assignment": True})
class State:
    order_id: OrderId
    customer_id: CustomerId
    order: Order = Field(init=False)
    customer: Customer = Field(init=False)
    payment: Payment = Field(init=False)


class LowFunds(Exception):
    pass
