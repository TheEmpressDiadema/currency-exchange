from currency_exchange.controller.dto import CurrencyDTO
from currency_exchange.model.models import Currency
from currency_exchange.model.repository import CurrencyRepository
from currency_exchange.model.value_objects import Code, Name, Sign


class CurrencyService:

    def __init__(self, currency_repo: CurrencyRepository):
        self._currency_repo = currency_repo

    def get_currency(self, code: str) -> CurrencyDTO:
        return CurrencyDTO.from_domain(self._currency_repo.get(code))

    def get_currencies(self) -> list[CurrencyDTO]:
        currencies = self._currency_repo.get_all()
        return [CurrencyDTO.from_domain(currency) for currency in currencies]

    def create_currency(self, code: str, name: str, sign: str) -> CurrencyDTO:
        currency = Currency(
            code=Code(code),
            name=Name(name),
            sign=Sign(sign)
        )
        return CurrencyDTO.from_domain(self._currency_repo.add(currency))