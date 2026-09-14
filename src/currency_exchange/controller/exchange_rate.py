from currency_exchange.exceptions import (
    CantGetCurrency,
    CantGetExchangeRate,
    CantInsertExchangeRate,
    CantUpdateExchangeRate,
    ExchangeRateAlreadyExists,
    IncorrectInput
)
from currency_exchange.server.structures import HttpRequest, HttpResponse
from currency_exchange.services.exchange_rate import ExchangeRateService
from currency_exchange.view.encoder import create_list_view, create_view


class ExchangeRateController:

    def __init__(self, exchange_rate_service: ExchangeRateService):
        self._exchange_rate_service = exchange_rate_service

    def create_exchange_rate(self, request: HttpRequest) -> HttpResponse:
        try:
            base_currency_code = request.body.get('baseCurrencyCode')
            target_currency_code = request.body.get('targetCurrencyCode')
            rate = request.body.get('rate')

            if all([
                isinstance(base_currency_code, str),
                isinstance(target_currency_code, str),
                isinstance(rate, str)
            ]):
                base_currency_code = base_currency_code.strip()
                target_currency_code = target_currency_code.strip()
                rate = rate.strip()
            else:
                raise IncorrectInput('One or more fields (baseCurrencyCode, targetCurrencyCode, rate) is incorrect')

            if len(base_currency_code) == 0:
                raise IncorrectInput('Base code should be 3 symbol length')

            if len(target_currency_code) == 0:
                raise IncorrectInput('Target code should be 3 symbol length')

            try:
                rate = float(rate)
            except (TypeError, ValueError):
                raise IncorrectInput("Incorrect rate value input")

            dto = self._exchange_rate_service.create_exchange_rate(
                    base_currency_code,
                    target_currency_code,
                    rate
                    )
        except (IncorrectInput, CantInsertExchangeRate, ValueError) as error:
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
        except CantGetCurrency as error:
            return HttpResponse(
                code=404,
                message=create_view(
                    {'message' : str(error)}
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
            codes = request.path_params.get('codes')

            if isinstance(codes, str):
                codes = codes.strip()
            else:
                raise IncorrectInput('Codes param is empty')

            if len(codes) < 6:
                raise IncorrectInput('Incorrect code pair input')

            base_currency_code = codes[:3]
            target_currency_code = codes[3:]

            rate = request.body.get('rate')

            try:
                rate = float(rate)
            except (TypeError, ValueError):
                raise IncorrectInput("Incorrect rate input")

            dto = self._exchange_rate_service.update_exchange_rate(
                base_currency_code,
                target_currency_code,
                rate
            )
        except (IncorrectInput, CantUpdateExchangeRate, ValueError) as error:
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
                    {'message' : str(error)}
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

    def get_exchange_rate(self, request: HttpRequest) -> HttpResponse:
        try:
            codes = request.path_params.get('codes')

            if isinstance(codes, str):
                codes = codes.strip()
            else:
                raise IncorrectInput('Codes should be str value')

            if len(codes) < 6:
                IncorrectInput('Incorrect code pair input')
            
            base_currency_code = codes[:3]
            target_currency_code = codes[3:]

            dto = self._exchange_rate_service.get_exchange_rate(
                base_currency_code,
                target_currency_code
                )
            
        except IncorrectInput as error:
            return HttpResponse(
                code=400,
                message=create_view(
                    {'message' : str(error)}
                )
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