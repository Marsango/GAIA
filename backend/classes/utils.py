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
            raise TypeError(f'Error with values of {key}')
        if isinstance(function_parameters[key], str):
            if function_parameters[key] == '':
                raise ValueError(f'String is empty')


def to_dict(_object: Any) -> dict[str, Any]:
    aux_dict: dict[str, Any] = {}
    _object = _object.__dict__
    for key in _object:
        aux_dict[key.split('__')[1]] = _object[key]
    return aux_dict
