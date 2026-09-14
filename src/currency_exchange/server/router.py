from collections.abc import Callable
from dataclasses import dataclass

from currency_exchange.server.structures import HttpRequest, HttpResponse
from currency_exchange.view.encoder import create_view


@dataclass(frozen=True)
class Route:
    method: str
    path: str
    func: Callable[..., HttpResponse]

class Router:

    def __init__(self) -> None:
        self._routes: list[Route] = []

    def register_route(self, route: Route) -> None:
        if route not in self._routes:
            self._routes.append(route)

    def _get_route(self, request: HttpRequest) -> Route | None:
        request_path = request.path.split('/')[1:]

        for route in self._routes:
            route_path = route.path.split('/')[1:]

            if request.method != route.method:
                continue

            if len(route_path) != len(request_path):
                continue

            is_match = True

            for expected, requested in zip(route_path, request_path):
                if expected.startswith('{') and expected.endswith('}'):
                    continue
                if expected != requested:
                    is_match = False


            if is_match:
                return Route(
                    method=route.method,
                    path=request.path,
                    func=route.func
                )
        return None

    def execute_route(self, request: HttpRequest) -> HttpResponse:
        response = HttpResponse(
            code=404,
            message=create_view(
                {'message' : 'Not Found'}
            )
        )
        route = self._get_route(request)
        if route is None:
            return response
        return route.func(request)