from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any
from urllib.parse import parse_qsl, urlparse

from currency_exchange.server.router import Router
from currency_exchange.server.structures import HttpRequest, HttpResponse


def run_server(host: str, port: int, handler_class: type[BaseHTTPRequestHandler]) -> None:
    http_server = HTTPServer((host, port), handler_class)

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        print('Работа сервера прекращена')
    http_server.server_close()

def create_handler(router: Router) -> type[BaseHTTPRequestHandler]:

    class RequestHandler(BaseHTTPRequestHandler):

        def _parse_body(self) -> dict[str, Any]:
            content_length = int(self.headers.get('Content-Length', 0))
            data = parse_qsl(self.rfile.read(content_length).decode('utf-8'))
            return dict(data)

        def _send_response(self, response: HttpResponse) -> None:
            self.send_response(response.code)

            for key, value in response.headers.items():
                self.send_header(key, value)
            self.end_headers()

            self.wfile.write(response.message.encode('utf-8'))

        def _parse_query(self, query: str) -> dict[str, Any]:
            params = dict(parse_qsl(query))
            for k,v in params.items():
                if v.startswith('$'):
                    params[k] = v[1:]
            return params

        def _parse_path(self, path: str) -> dict[str, Any]:
            result: dict[str, Any] = {}
            parsed_path = path.split('/')[1:]
            if len(parsed_path) == 2:
                if len(parsed_path[1]) == 3:
                    result['code'] = parsed_path[1]
                if len(parsed_path[1]) == 6:
                    result['codes'] = parsed_path[1]
            return result

        def _create_request(self) -> HttpRequest:
            url = urlparse(self.path)

            body: dict[str, Any] = self._parse_body()
            params: dict[str, Any] = self._parse_query(url.query)
            path_params: dict[str, Any] = self._parse_path(url.path)

            return HttpRequest(
                method=self.command,
                path=url.path,
                body=body,
                params=params,
                path_params=path_params
            )

        def _handle_request(self, request: HttpRequest) -> None:
            self._send_response(router.execute_route(request))
            
        def do_GET(self) -> None:
            self._handle_request(self._create_request())

        def do_POST(self) -> None:
            self._handle_request(self._create_request())

        def do_PATCH(self) -> None:
            self._handle_request(self._create_request())

    return RequestHandler