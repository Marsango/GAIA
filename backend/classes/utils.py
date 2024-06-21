import json
from typing import Any


def read_current_stored_config() -> dict[str, float]:
    with open("config.json", "r") as file:
        return json.load(file)


def verify_type(type_hints: dict[str, Any], function_parameters: dict[str, Any]) -> None:
    for key in type_hints:
        if key == 'return':
            continue
        if not isinstance(function_parameters[key], type_hints[key]):
            raise TypeError
