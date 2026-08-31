import json
from typing import Any


def create_list_view(dtos: list[dict[str, Any]]) -> str:
    result = []
    for dto in dtos:
        result.append(json.loads(create_view(dto)))
    return json.dumps(result, indent=4, ensure_ascii=False)

def create_view(dto_dict: dict[str, Any]) -> str:
    result = {}
    for key, value in dto_dict.items():
        result[key] = value
    return json.dumps(result, indent=4, ensure_ascii=False)