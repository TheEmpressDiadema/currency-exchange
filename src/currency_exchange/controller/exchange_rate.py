from currency_exchange.exceptions import (
    CantGetExchangeRate,
    CantInsertExchangeRate,
    CantUpdateExchangeRate,
    ExchangeRateAlreadyExists,
)
from currency_exchange.server.structures import HttpRequest, HttpResponse
from currency_exchange.services.exchange_rate import ExchangeRateService
from currency_exchange.view.encoder import create_list_view, create_view


class ExchangeRateController:

    def __init__(self, exchange_rate_service: ExchangeRateService):
        self._exchange_rate_service = exchange_rate_service

    def create_exchange_rate(self, request: HttpRequest) -> HttpResponse:
        try:
            base_currency_code = request.body['baseCurrencyCode']
            target_currency_code = request.body['targetCurrencyCode']
            rate = request.body['rate']
            dto = self._exchange_rate_service.create_exchange_rate(
                    base_currency_code,
                    target_currency_code,
                    rate
                    )
        except (CantInsertExchangeRate, ValueError) as error:
           return HttpResponse(
               code=400,
               message=create_view(
                    {
                        'message' : str(error)
                    }
                )
           )
        except ExchangeRateAlreadyExists as error:
            return HttpResponse(
                code=409,
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
            code=201,
            message=create_view(dto.as_dict())
        )

    def update_exchange_rate(self, request: HttpRequest) -> HttpResponse:
        try:
            codes = request.path_params['codes']
            base_currency_code = codes[:3]
            target_currency_code = codes[3:]
            rate = request.body['rate']
            dto = self._exchange_rate_service.update_exchange_rate(
                base_currency_code,
                target_currency_code,
                rate
            )
        except (CantUpdateExchangeRate, ValueError) as error:
            return HttpResponse(
                code=400,
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
            code=201,
            message=create_view(dto.as_dict())
        )

    def get_exchange_rate(self, request: HttpRequest) -> HttpResponse:
        try:
            codes = request.path_params['codes']
            base_currency_code = codes[:3]
            target_currency_code = codes[3:]
            dto = self._exchange_rate_service.get_exchange_rate(
                base_currency_code,
                target_currency_code
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

    def get_exchange_rates(self, request: HttpRequest | None = None) -> HttpResponse:
        try:
            dtos = self._exchange_rate_service.get_exchange_rates()
            result = [dto.as_dict() for dto in dtos]
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
            message=create_list_view(result)
        )