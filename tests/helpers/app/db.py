from app.entities import Price
from app.entities import Profile


class ProfileTable:
    @staticmethod
    def where(pk):
        return type("Where", (), {"select": lambda: Profile(pk, 100)})


class PriceTable:
    @staticmethod
    def where(pk):
        return type("Where", (), {"select": lambda: Price(pk, 99, 30)})
