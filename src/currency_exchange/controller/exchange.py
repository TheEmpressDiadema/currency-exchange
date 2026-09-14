from currency_exchange.exceptions import CantGetExchangeRate
from currency_exchange.server.structures import HttpRequest, HttpResponse
from currency_exchange.services.exchange import ExchangeService
from currency_exchange.view.encoder import create_view


class ExchangeController:

    def __init__(self, exchange_service: ExchangeService):
        self._exchange_service = exchange_service

    def get_exchange(self, request: HttpRequest) -> HttpResponse:
        try:
            base_currency_code = request.params['from']
            target_currency_code = request.params['to']
            amount = float(request.params['amount'])
            dto = self._exchange_service.get_exchange(
                base_currency_code,
                target_currency_code,
                amount
            )
        except CantGetExchangeRate:
            try:
                dto = self._exchange_service.get_reversed_exchange(
                    target_currency_code, 
                    base_currency_code, 
                    amount
                    )
            except CantGetExchangeRate:
                try:
                    dto = self._exchange_service.get_exchange_throgh_dollar(
                        base_currency_code,
                        target_currency_code,
                        amount
                    )
                except CantGetExchangeRate as error:
                    return HttpResponse(
                        code=404,
                        message=create_view(
                    {
                        'message' : str(error)
                    }
                )
                    )
        except Exception as error:
            return HttpResponse(
                code=500,
                message=create_view(
                    {
                        'message' : str(error)
                    }
                )
            )

        return HttpResponse(
            code=200,
            message=create_view(dto.as_dict())
        )