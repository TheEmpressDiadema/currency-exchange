import json
from typing import Any


def create_list_view(dtos: list[dict[str, Any]]) -> str:
    result = []
    for dto in dtos:
        result.append(json.loads(create_view(dto)))
    return json.dumps(result, indent=4, ensure_ascii=False)

def create_view(dict_object: dict[str, Any]) -> str:
    return json.dumps(dict_object, indent=4, ensure_ascii=False)