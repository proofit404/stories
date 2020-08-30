from app.entities import Category
from app.entities import Price
from app.entities import Profile
from app.entities import Subscription
from app.entities import Token


async def load_promo_code(category):
    pass


async def load_token():
    return Token()


async def load_category(primary_key):
    names = {1: "Books", 2: "Movies"}
    costs = {1: 7, 2: 17}
    return Category(
        primary_key=primary_key, name=names[primary_key], cost=costs[primary_key]
    )


async def load_price(primary_key):
    costs = {1: 7, 2: 17}
    periods = {1: 30, 2: 30}
    return Price(
        primary_key=primary_key, cost=costs[primary_key], period=periods[primary_key]
    )


async def load_profile(primary_key):
    balances = {1: 8, 2: 8}
    return Profile(primary_key=primary_key, balance=balances[primary_key])


async def decrease_balance(profile, cost):
    pass


async def save_profile(profile):
    pass


async def calculate_period(period):
    pass


async def create_subscription(profile, category, expires=None):
    keys = {(1, 1): 9}
    return Subscription(primary_key=keys[(profile.primary_key, category.primary_key)])


async def load_subscription(category_id, profile_id):
    keys = {(1, 1): 1, (2, 1): 7}
    return Subscription(primary_key=keys[(category_id, profile_id)])


async def send_notification(kind, profile, category_name):
    pass
