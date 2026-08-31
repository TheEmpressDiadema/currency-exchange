from decimal import ROUND_HALF_UP, Decimal

from currency_exchange.controller.dto import CurrencyDTO, ExchangeDTO
from currency_exchange.model.repository import ExchangeRateRepository
from currency_exchange.model.utils import from_decimal, to_decimal


class ExchangeService:

    def __init__(self, exchange_rate_repo: ExchangeRateRepository):
        self._exchange_rate_repo = exchange_rate_repo

    def get_exchange(self, 
                    base_currency_code: str, 
                    target_currency_code: str, 
                    amount: float) -> ExchangeDTO:
        exchange_rate = self._exchange_rate_repo.get(base_currency_code, target_currency_code)
        rate = exchange_rate.rate.value
        result = to_decimal(amount)*rate
        return ExchangeDTO(
            base_currency=CurrencyDTO.from_domain(exchange_rate.base_currency),
            target_currency=CurrencyDTO.from_domain(exchange_rate.target_currency),
            rate=from_decimal(rate),
            amount=amount,
            converted_amount=from_decimal(result.quantize(Decimal('0.000001'), ROUND_HALF_UP))
        )

    def get_reversed_exchange(self, 
                              target_currency_code: str, 
                              base_currency_code: str, 
                              amount: float) -> ExchangeDTO:
        exchange_rate = self._exchange_rate_repo.get(target_currency_code, base_currency_code)
        rate = exchange_rate.rate.value
        result = to_decimal(amount)/rate
        return ExchangeDTO(
            base_currency=CurrencyDTO.from_domain(exchange_rate.base_currency),
            target_currency=CurrencyDTO.from_domain(exchange_rate.target_currency),
            rate=from_decimal(rate),
            amount=amount,
            converted_amount=from_decimal(result.quantize(Decimal('0.000001'), ROUND_HALF_UP))
        )

    def get_exchange_throgh_dollar(self, 
                                base_currency_code: str, 
                                target_currency_code: str, 
                                amount: float) -> ExchangeDTO:
        usd_to_base = self._exchange_rate_repo.get("USD", base_currency_code)
        usd_to_target = self._exchange_rate_repo.get("USD", target_currency_code)

        base_rate = usd_to_base.rate.value
        target_rate = usd_to_target.rate.value

        rate = target_rate/base_rate
        result = rate*to_decimal(amount)

        return ExchangeDTO(
            base_currency=CurrencyDTO.from_domain(usd_to_base.target_currency),
            target_currency=CurrencyDTO.from_domain(usd_to_target.target_currency),
            rate=from_decimal(rate), 
            amount=amount,
            converted_amount=from_decimal(result)
        )