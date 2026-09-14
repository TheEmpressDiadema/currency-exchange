from dataclasses import dataclass, field
from typing import Any


@dataclass
class HttpRequest:

    method: str
    path: str
    body: dict[str, Any]
    params: dict[str, str | None]
    path_params: dict[str, str | None]


@dataclass
class HttpResponse:

    code: int
    message: str
    headers: dict[str, str] = field(
        default_factory=lambda : (
            {
                "Content-type" : "application/json",
                "Access-Control-Allow-Origin" : "*",
                "Access-Control-Allow-Methods" : "GET, POST, PATCH, OPTIONS",
                "Access-Control-Allow-Headers" : "Content-Type"
            }
        )
    )
