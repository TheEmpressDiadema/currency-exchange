from currency_exchange.controller.currency import CurrencyController
from currency_exchange.controller.exchange import ExchangeController
from currency_exchange.controller.exchange_rate import ExchangeRateController
from currency_exchange.init_db import init_db
from currency_exchange.model.sqlite_repository import (
    CurrencySqliteRepository,
    ExchangeRateSqliteRepository,
)
from currency_exchange.server.router import Route, Router
from currency_exchange.server.server import create_handler, run_server
from currency_exchange.services.currency import CurrencyService
from currency_exchange.services.exchange import ExchangeService
from currency_exchange.services.exchange_rate import ExchangeRateService


def main() -> None:
    data_dir = 'data'
    data_file = 'data.db'
    init_db(data_dir, data_file)
    router = Router()

    currency_repo = CurrencySqliteRepository(f'{data_dir}/{data_file}')
    exchange_rate_repo = ExchangeRateSqliteRepository(f'{data_dir}/{data_file}')

    exchange_service = ExchangeService(exchange_rate_repo)
    currency_service = CurrencyService(currency_repo)
    exchange_rate_service = ExchangeRateService(exchange_rate_repo, currency_repo)

    cur_controller = CurrencyController(currency_service)
    exchange_rate_controller = ExchangeRateController(exchange_rate_service)
    exchange_controller = ExchangeController(exchange_service)

    router.register_route(
        Route(
            method='GET',
            path='/currencies',
            func=cur_controller.get_currencies
        )
    )
    router.register_route(
        Route(
            method='GET',
            path='/currency/{code}',
            func=cur_controller.get_currency
        )
    )
    router.register_route(
        Route(
            method='POST',
            path='/currencies',
            func=cur_controller.create_currency
        )
    )
    router.register_route(
        Route(
            method='GET',
            path='/exchangeRates',
            func=exchange_rate_controller.get_exchange_rates
        )
    )
    router.register_route(
        Route(
            method='GET',
            path='/exchangeRate/{codes}',
            func=exchange_rate_controller.get_exchange_rate
        )
    )
    router.register_route(
        Route(
            method='POST',
            path='/exchangeRates',
            func=exchange_rate_controller.create_exchange_rate
        )
    )
    router.register_route(
        Route(
            method='PATCH',
            path='/exchangeRate/{codes}',
            func=exchange_rate_controller.update_exchange_rate
        )
    )
    router.register_route(
        Route(
            method='GET',
            path='/exchange',
            func=exchange_controller.get_exchange
        )
    )
    
    handler_class = create_handler(router)
    run_server('localhost', 8000, handler_class)