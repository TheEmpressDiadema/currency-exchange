from currency_exchange.controller.dto import ExchangeRateDTO
from currency_exchange.model.models import ExchangeRate
from currency_exchange.model.repository import (
    CurrencyRepository,
    ExchangeRateRepository,
)
from currency_exchange.model.utils import to_decimal
from currency_exchange.model.value_objects import Rate


class ExchangeRateService:

    def __init__(self, exchange_rate_repo: ExchangeRateRepository, currency_repo: CurrencyRepository):
        self._exchange_rate_repo = exchange_rate_repo
        self._currency_repo = currency_repo

    def get_exchange_rate(self, base_currency_code: str, target_currency_code: str) -> ExchangeRateDTO:
        return ExchangeRateDTO.from_domain(
            self._exchange_rate_repo.get(base_currency_code, target_currency_code)
        )

    def get_exchange_rates(self) -> list[ExchangeRateDTO]:
        exchange_rates = self._exchange_rate_repo.get_all()
        return [ExchangeRateDTO.from_domain(exchange_rate) for exchange_rate in exchange_rates]

    def create_exchange_rate(self, 
                            base_currency_code: str, 
                            target_currency_code: str, 
                            rate: float) -> ExchangeRateDTO:
        base_currency = self._currency_repo.get(base_currency_code)
        target_currency = self._currency_repo.get(target_currency_code)
        exchange_rate = ExchangeRate(
            base_currency=base_currency,
            target_currency=target_currency,
            rate=Rate(to_decimal(rate))
        )
        return ExchangeRateDTO.from_domain(self._exchange_rate_repo.add(exchange_rate))

    def update_exchange_rate(self, 
                            base_currency_code: str, 
                            target_currency_code: str, 
                            rate: float) -> ExchangeRateDTO:
        base_currency = self._currency_repo.get(base_currency_code)
        target_currency = self._currency_repo.get(target_currency_code)
        exchange_rate = ExchangeRate(
            base_currency=base_currency,
            target_currency=target_currency,
            rate=Rate(to_decimal(rate))
        )
        return ExchangeRateDTO.from_domain(self._exchange_rate_repo.update(exchange_rate))