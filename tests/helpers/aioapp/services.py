# -*- coding: utf-8 -*-
from enum import auto
from enum import Enum

from aioapp.repositories import create_subscription
from aioapp.repositories import decrease_balance
from aioapp.repositories import load_category
from aioapp.repositories import load_price
from aioapp.repositories import load_profile
from aioapp.repositories import load_subscription
from aioapp.repositories import save_profile
from aioapp.repositories import send_notification
from app.repositories import calculate_period
from stories import arguments
from stories import Failure
from stories import Result
from stories import story
from stories import Success


class Subscription:
    """Buy subscription for certain category."""

    @story
    @arguments("category_id", "price_id", "profile_id")
    def buy(I):

        I.find_category
        I.find_price
        I.find_profile
        I.check_balance
        I.persist_payment
        I.persist_subscription
        I.send_subscription_notification
        I.show_category

    async def find_category(self, ctx):

        ctx.category = await load_category(ctx.category_id)
        return Success()

    async def find_price(self, ctx):

        ctx.price = await load_price(ctx.price_id)
        return Success()

    async def find_profile(self, ctx):

        ctx.profile = await load_profile(ctx.profile_id)
        return Success()

    async def check_balance(self, ctx):

        if ctx.profile.balance > ctx.price.cost:
            return Success()
        else:
            return Failure()

    async def persist_payment(self, ctx):

        await decrease_balance(ctx.profile, ctx.price.cost)
        await save_profile(ctx.profile)
        return Success()

    async def persist_subscription(self, ctx):

        expires = calculate_period(ctx.price.period)
        ctx.subscription = await create_subscription(ctx.profile, ctx.category, expires)
        return Success()

    async def send_subscription_notification(self, ctx):

        ctx.notification = await send_notification(
            "subscription", ctx.profile, ctx.category.name
        )
        return Success()

    async def show_category(self, ctx):

        return Result(ctx.category)


class ShowCategory:
    """Show category entries."""

    @story
    @arguments("category_id", "profile_id")
    def show(I):

        I.find_subscription
        I.check_expiration
        I.find_category
        I.show_category

    async def find_subscription(self, ctx):

        subscription = await load_subscription(ctx.category_id, ctx.profile_id)
        if subscription:
            ctx.subscription = subscription
            return Success()
        else:
            return Failure(Errors.forbidden)

    async def check_expiration(self, ctx):

        if ctx.subscription.is_expired():
            return Failure(Errors.forbidden)
        else:
            return Success()

    async def find_category(self, ctx):

        category = await load_category(ctx.category_id)
        if category:
            ctx.category = category
            return Success()
        else:
            return Failure(Errors.not_found)

    async def show_category(self, ctx):

        return Result(ctx.category)


@ShowCategory.show.failures
class Errors(Enum):

    forbidden = auto()
    not_found = auto()
