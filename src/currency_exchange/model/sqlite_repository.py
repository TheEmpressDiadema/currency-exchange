import sqlite3
from contextlib import closing
from typing import Any, override

from currency_exchange.exceptions import *
from currency_exchange.model.models import Currency, ExchangeRate
from currency_exchange.model.repository import (
    CurrencyRepository,
    ExchangeRateRepository,
)
from currency_exchange.model.utils import from_decimal, to_decimal
from currency_exchange.model.value_objects import Code, Name, Rate, Sign


class CurrencySqliteRepository(CurrencyRepository):

    def __init__(self, db_path: str):
        self._db_path = db_path

    @override
    def add(self, currency: Currency) -> Currency:
        query = '''
        INSERT OR IGNORE INTO currency(code, name, sign)
        VALUES (?, ?, ?) RETURNING *'''
        params = (
            currency.code.value,
            currency.name.value,
            currency.sign.value
        )
        with sqlite3.connect(self._db_path) as con, closing(con.cursor()) as cursor:
            try:
                result = cursor.execute(query, params).fetchone()
            except sqlite3.IntegrityError:
                raise CantInsertCurrency("Can't insert currency - Db broken :(")

        if result is None:
            raise CurrencyAlreadyExists("Can't insert Currency - already exists")
        _id, _code, _name, _sign = result
        return Currency(
            code=Code(_code),
            name=Name(_name),
            sign=Sign(_sign),
            id=_id
        )

    @override
    def get(self, code: str) -> Currency:
        query = '''SELECT * FROM currency
        WHERE code=?'''
        params = (
            code,
        )
        with sqlite3.connect(self._db_path) as con, closing(con.cursor()) as cursor:
            result = cursor.execute(query, params).fetchone()

        if result is None:
            raise CantGetCurrency("Currency doesn't exist")
        
        _id, _code, name, sign = result
        return Currency(
                    code=Code(_code),
                    name=Name(name),
                    sign=Sign(sign),
                    id=_id
                )

    @override
    def get_all(self) -> list[Currency]:
        query = '''
        SELECT * FROM currency
        '''
        with sqlite3.connect(self._db_path) as con, closing(con.cursor()) as cursor:
            result = cursor.execute(query).fetchall()

        if result is None:
            raise CantGetCurrency('Currency table is empty')
        
        currencies = []
        for _id, code, name, sign in result:
            currencies.append(
                Currency(
                    code=Code(code),
                    name=Name(name),
                    sign=Sign(sign),
                    id=_id
                )
            )
        return currencies

class ExchangeRateSqliteRepository(ExchangeRateRepository):

    def __init__(self, db_path: str):
        self._db_path = db_path

    def _parse_upsert_row(self, exchange_rate: ExchangeRate, result: Any) -> ExchangeRate:
        _id, base_currency_id, target_currency_id, _rate = result

        base_currency = Currency(
            code=exchange_rate.base_currency.code,
            name=exchange_rate.base_currency.name,
            sign=exchange_rate.base_currency.sign,
            id=base_currency_id
        )
        target_currency = Currency(
            code=exchange_rate.target_currency.code,
            name=exchange_rate.target_currency.name,
            sign=exchange_rate.target_currency.sign,
            id=target_currency_id
        )

        return ExchangeRate(
            base_currency=base_currency,
            target_currency=target_currency,
            rate=Rate(to_decimal(_rate)),
            id=_id
        )


    def _parse_row(self, result: Any) -> ExchangeRate:
        (_id, 
        base_currency_id,
        base_currency_code,
        base_currency_name,
        base_currency_sign, 
        target_currency_id,
        target_currency_code,
        target_currency_name,
        target_currency_sign,
        _rate
        ) = result
        
        base_currency = Currency(
            code=Code(base_currency_code),
            name=Name(base_currency_name),
            sign=Sign(base_currency_sign),
            id=base_currency_id
        )

        target_currency = Currency(
            code=Code(target_currency_code),
            name=Name(target_currency_name),
            sign=Sign(target_currency_sign),
            id=target_currency_id
        )

        return ExchangeRate(
            base_currency=base_currency,
            target_currency=target_currency,
            rate=Rate(to_decimal(_rate)),
            id=_id
        )

    @override
    def add(self, exchange_rate: ExchangeRate) -> ExchangeRate:
    
        query = '''INSERT OR IGNORE INTO exchange_rate(base_currency_id, target_currency_id, rate)
        VALUES (?, ?, ?) RETURNING *'''
        params = (
            exchange_rate.base_currency.id,
            exchange_rate.target_currency.id,
            from_decimal(exchange_rate.rate.value)
        )
        with sqlite3.connect(self._db_path) as con, closing(con.cursor()) as cursor:
            try:
                result = cursor.execute(query, params).fetchone()
            except sqlite3.IntegrityError:
                raise CantInsertExchangeRate("Can't insert ExchangeRate - Db broken :(")

        print(result)

        if result is None:
            raise ExchangeRateAlreadyExists("Can't insert ExchangeRate - already exists")

        return self._parse_upsert_row(exchange_rate, result)
        

    @override
    def update(self, exchange_rate: ExchangeRate) -> ExchangeRate:
        query = '''UPDATE exchange_rate
        SET rate=?
        WHERE base_currency_id=(SELECT id FROM currency WHERE code=?)
        AND target_currency_id=(SELECT id FROM currency WHERE code=?)
        RETURNING *'''
        params = (
            from_decimal(exchange_rate.rate.value),
            exchange_rate.base_currency.code.value,
            exchange_rate.target_currency.code.value
        )
        with sqlite3.connect(self._db_path) as con, closing(con.cursor()) as cursor:
            try:
                result = cursor.execute(query, params).fetchone()
            except sqlite3.DatabaseError:
                raise CantUpdateExchangeRate("Can't update ExchangeRate - db broken :(")

        if result is None:
            raise CantUpdateExchangeRate("Can't update ExchangeRate, not found")

        return self._parse_upsert_row(exchange_rate, result)

    @override
    def get(self, base_currency_code: str, target_currency_code: str) -> ExchangeRate:
        query = '''SELECT
            exchange_rate.id,
            base_currency.id,
            base_currency.code,
            base_currency.name,
            base_currency.sign,
            target_currency.id,
            target_currency.code,
            target_currency.name,
            target_currency.sign,
            exchange_rate.rate
            FROM exchange_rate
            INNER JOIN currency AS base_currency ON exchange_rate.base_currency_id=base_currency.id
            INNER JOIN currency AS target_currency ON exchange_rate.target_currency_id=target_currency.id
            WHERE base_currency.code=? AND target_currency.code=?'''
        params = (
            base_currency_code,
            target_currency_code
        )
        with sqlite3.connect(self._db_path) as con, closing(con.cursor()) as cursor:
            result = cursor.execute(query, params).fetchone()

        if result is None:
            raise CantGetExchangeRate("No exchange rate found")
        
        return self._parse_row(result)

    @override
    def get_all(self) -> list[ExchangeRate]:
        query = '''SELECT
            exchange_rate.id,
            base_currency.id,
            base_currency.code,
            base_currency.name,
            base_currency.sign,
            target_currency.id,
            target_currency.code,
            target_currency.name,
            target_currency.sign,
            exchange_rate.rate
            FROM exchange_rate
            INNER JOIN currency AS base_currency ON exchange_rate.base_currency_id=base_currency.id
            INNER JOIN currency AS target_currency ON exchange_rate.target_currency_id=target_currency.id'''
        with sqlite3.connect(self._db_path) as con, closing(con.cursor()) as cursor:
            result = cursor.execute(query).fetchall()
        exchange_rates = []

        if result is None:
            raise CantGetExchangeRate('ExchangeRate table is empty')
        
        for row in result:
            exchange_rates.append(self._parse_row(row))
        return exchange_rates