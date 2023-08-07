from collections.abc import Callable
from dataclasses import dataclass
from types import SimpleNamespace as State
from typing import assert_type

from app.entities import Customer
from app.entities import CustomerId
from app.entities import Order
from app.entities import OrderId
from app.entities import Payment
from app.repositories import create_payment
from app.repositories import load_customer
from app.repositories import load_order

from stories import I
from stories import Story


@dataclass
class Purchase(Story):
    I.find_order
    I.find_customer
    I.check_balance
    I.persist_payment

    def find_order(self, state: State) -> None:
        state.order = self.load_order(state.order_id)

    def find_customer(self, state: State) -> None:
        state.customer = self.load_customer(state.customer_id)

    def check_balance(self, state: State) -> None:
        if not state.order.affordable_for(state.customer):
            raise Exception

    def persist_payment(self, state: State) -> None:
        state.payment = self.create_payment(state.order_id, state.customer_id)

    load_order: Callable[[OrderId], Order]
    load_customer: Callable[[CustomerId], Customer]
    create_payment: Callable[[OrderId, CustomerId], Payment]


purchase = Purchase(
    load_order=load_order,
    load_customer=load_customer,
    create_payment=create_payment,
)


state = State(order_id=1, customer_id=1)


purchase(state)


assert_type(state.payment, Payment)
print(state.payment.was_received())
