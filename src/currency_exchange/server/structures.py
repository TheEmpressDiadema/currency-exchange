from typing import Any
from dataclasses import dataclass, field


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
    headers: dict[str, str] = field(
        default_factory=lambda : (
            {
                "Content-type" : "application/json",
                "Access-Control-Allow-Origin" : "*"
            }
        )
    )
