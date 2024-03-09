from __future__ import annotations

from app.repositories import create_payment
from app.repositories import load_customer
from app.repositories import load_order
from app.usecases import CustomerId
from app.usecases import OrderId
from app.usecases import Purchase
from app.usecases import State
from stories import story


def test_story() -> None:
    purchase = Purchase(
        load_order=load_order,
        load_customer=load_customer,
        create_payment=create_payment,
    )

    state = State(order_id=OrderId(1), customer_id=CustomerId(1))

    with story(purchase) as seller:
        seller.find_order(state)
        seller.find_customer(state)
        seller.check_balance(state)
        seller.persist_payment(state)

    assert not state.payment.was_received()
