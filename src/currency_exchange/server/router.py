from collections.abc import Callable
from dataclasses import dataclass

from currency_exchange.server.structures import HttpRequest, HttpResponse


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

    def _match_route(self, request: HttpRequest) -> Route | None:
        for route in self._routes:
            if route.method == request.method and request.path == route.path:
                return route
        return None

    def execute_route(self, request: HttpRequest) -> HttpResponse:
        response = HttpResponse(
            code=404,
            message="Not Found"
        )
        route = self._match_route(request)
        if route is None:
            return response
        response = route.func(request)
        return response