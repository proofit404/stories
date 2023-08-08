from datetime import datetime

from aioapp.entities import Cost
from aioapp.entities import Customer
from aioapp.entities import CustomerId
from aioapp.entities import Order
from aioapp.entities import OrderId
from aioapp.entities import Payment
from aioapp.entities import Product


async def load_order(order_id: OrderId) -> Order:
    """Perform database query."""
    names = {1: "Books", 2: "Movies"}
    dates = {1: datetime(1999, 12, 31), 2: datetime(2000, 1, 1)}
    costs = {1: 7, 2: 17}
    return Order(
        product=Product(name=names[order_id]),
        cost=Cost(at=dates[order_id], amount=costs[order_id]),
    )


async def load_customer(customer_id: CustomerId) -> Customer:
    """Perform database query."""
    balances = {1: 8, 2: 8}
    return Customer(balance=balances[customer_id])


async def create_payment(customer_id: CustomerId, order_id: OrderId) -> Payment:
    """Perform database query."""
    dates = {(1, 1): datetime(1999, 12, 31)}
    return Payment(due_date=dates[(customer_id, order_id)])
