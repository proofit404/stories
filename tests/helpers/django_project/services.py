from enum import Enum, auto
from inspect import getfullargspec

from stories import Failure, Result, Success, arguments, story


class MethodDefinitionsType(type):
    def __getattr__(cls, attrname):
        if attrname in getfullargspec(cls.__init__).args:
            raise AttributeError
        else:
            return lambda self, ctx: Success()


class MethodDefinitions(metaclass=MethodDefinitionsType):
    pass


class Subscription:
    """Buy subscription for certain category."""

    @story
    @arguments("category_id", "price_id", "user_id")
    def buy(I):

        I.find_category
        I.find_price
        I.find_profile
        I.check_balance
        I.persist_payment
        I.persist_subscription
        I.send_subscription_notification
        I.show_category

    def find_category(self, ctx):

        category = load_category(ctx.category_id)
        return Success(category=category)

    def find_price(self, ctx):

        price = load_price(ctx.price_id)
        return Success(price=price)

    def find_profile(self, ctx):

        profile = load_profile(ctx.user_id)
        return Success(profile=profile)

    def check_balance(self, ctx):

        if ctx.profile.balance > ctx.price.cost:
            return Success()
        else:
            return Failure()

    def persist_payment(self, ctx):

        decrease_balance(ctx.profile, ctx.price.cost)
        save_profile(ctx.profile)
        return Success()

    def persist_subscription(self, ctx):

        expires = calculate_period(ctx.price.period)
        subscription = create_subscription(ctx.profile, ctx.category, expires)
        return Success(subscription=subscription)

    def send_subscription_notification(self, ctx):

        notification = send_notification("subscription", ctx.profile, ctx.category.name)
        return Success(notification=notification)

    def show_category(self, ctx):

        return Result(ctx.category)


class ShowCategory:
    """Show category entries."""

    @story
    @arguments("category_id", "user_id")
    def show(I):

        I.find_subscription
        I.check_expiration
        I.find_category
        I.show_category

    def find_subscription(self, ctx):

        subscription = load_subscription(ctx.category_id, ctx.user_id)
        if subscription:
            return Success(subscription=subscription)
        else:
            return Failure(Errors.forbidden)

    def check_expiration(self, ctx):

        if ctx.subscription.is_expired():
            return Failure(Errors.forbidden)
        else:
            return Success()

    def find_category(self, ctx):

        category = load_category(ctx.category_id)
        if category:
            return Success(category=category)
        else:
            return Failure(Errors.not_found)

    def show_category(self, ctx):

        return Result(ctx.category)


@ShowCategory.show.failures
class Errors(Enum):

    forbidden = auto()
    not_found = auto()