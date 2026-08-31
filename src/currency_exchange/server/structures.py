from dataclasses import dataclass, field
from typing import Any


@dataclass
class HttpRequest:

    method: str
    path: str
    body: dict[str, Any]
    params: dict[str, Any]
    path_params: dict[str, Any]


@dataclass
class HttpResponse:

    code: int
    message: str
    keyword: str = field(default="Content-type")
    value: str = field(default="application/json")