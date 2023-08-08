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

    class PurchaseState(State):
        order_id: OrderId
        customer_id: CustomerId

        order: Order
        customer: Customer
        payment: Payment

    def find_order(self, state: PurchaseState) -> None:
        state.order = self.load_order(state.order_id)

    def find_customer(self, state: PurchaseState) -> None:
        state.customer = self.load_customer(state.customer_id)

    def check_balance(self, state: PurchaseState) -> None:
        if not state.order.affordable_for(state.customer):
            raise Exception

    def persist_payment(self, state: PurchaseState) -> None:
        state.payment = self.create_payment(state.customer_id, state.order_id)

    load_order: Callable[[OrderId], Order]
    load_customer: Callable[[CustomerId], Customer]
    create_payment: Callable[[CustomerId, OrderId], Payment]


purchase = Purchase(
    load_order=load_order,
    load_customer=load_customer,
    create_payment=create_payment,
)

state = purchase.PurchaseState(order_id=1, customer_id=1)

purchase(state)

assert_type(state.payment, Payment)
print(state.payment.was_received())
