# -*- coding: utf-8 -*-
from app.entities import Price
from app.entities import Profile


class ProfileTable:
    @staticmethod
    def where(pk):
        async def select():
            return Profile(pk, 100)

        return type("Where", (), {"select": select})


class PriceTable:
    @staticmethod
    def where(pk):
        async def select():
            return Price(pk, 99, 30)

        return type("Where", (), {"select": select})
