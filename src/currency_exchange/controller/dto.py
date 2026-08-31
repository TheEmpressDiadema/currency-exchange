from dataclasses import dataclass
from typing import Any, Self

from currency_exchange.model.models import Currency, ExchangeRate
from currency_exchange.model.utils import from_decimal


@dataclass
class CurrencyDTO:

    id: int
    name: str
    code: str
    sign: str

    @classmethod
    def from_domain(cls, currency: Currency) -> Self:
        return cls(
            currency.id,
            currency.name.value,
            currency.code.value,
            currency.sign.value
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name" : self.name,
            "code" : self.code,
            "sign" : self.sign
        }

@dataclass
class ExchangeRateDTO:

    id: int
    base_currency: CurrencyDTO
    target_currency: CurrencyDTO
    rate: float

    @classmethod
    def from_domain(cls, exchange_rate: ExchangeRate) -> Self:
        return cls(
            exchange_rate.id,
            CurrencyDTO.from_domain(exchange_rate.base_currency),
            CurrencyDTO.from_domain(exchange_rate.target_currency),
            from_decimal(exchange_rate.rate.value)
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "id" : self.id,
            "baseCurrency" : self.base_currency.as_dict(),
            "targetCurrency" : self.target_currency.as_dict(),
            "rate" : self.rate
        }

@dataclass
class ExchangeDTO:

    base_currency: CurrencyDTO
    target_currency: CurrencyDTO
    rate: float
    amount: float
    converted_amount: float

    def as_dict(self) -> dict[str, Any]:
        return {
            "baseCurrency" : self.base_currency.as_dict(),
            "targetCurrency" : self.target_currency.as_dict(),
            "rate" : self.rate,
            "amount" : self.amount,
            "convertedAmount" : self.converted_amount
        }