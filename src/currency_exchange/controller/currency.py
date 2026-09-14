from currency_exchange.exceptions import (
    CantGetCurrency,
    CantInsertCurrency,
    CurrencyAlreadyExists,
)
from currency_exchange.server.structures import HttpRequest, HttpResponse
from currency_exchange.services.currency import CurrencyService
from currency_exchange.view.encoder import create_list_view, create_view


class CurrencyController:

    def __init__(self, currency_service: CurrencyService):
        self._currency_service = currency_service

    def create_currency(self, request: HttpRequest) -> HttpResponse:
        try:
            code = request.body['code']
            name = request.body['name']
            sign = request.body['sign']
            dto = self._currency_service.create_currency(code, name, sign)
        except (ValueError, CantInsertCurrency) as error:
            return HttpResponse(
                code=400,
                message=create_view(
                    {
                        'message' : str(error)
                    }
                )
            )
        except CurrencyAlreadyExists as error:
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

    def get_currency(self, request: HttpRequest) -> HttpResponse:
        try:
            code = request.path_params['code']
            dto = self._currency_service.get_currency(code)
        except ValueError as error:
            return HttpResponse(
                code=400,
                message=create_view(
                    {
                        'message' : str(error)
                    }
                )
            )
        except CantGetCurrency as error:
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

    def get_currencies(self, request: HttpRequest | None = None) -> HttpResponse:
        try:
            dtos = self._currency_service.get_currencies()
            result = [dto.as_dict() for dto in dtos]
        except CantGetCurrency as error:
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