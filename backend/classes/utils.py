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
            raise TypeError(f"Error with values of '{key}'")
        if isinstance(function_parameters[key], str):
            if function_parameters[key] == '':
                raise ValueError(f"Field '{key}' is empty")


def to_dict(_object: Any) -> dict[str, Any]:
    aux_dict: dict[str, Any] = {}
    _object = _object.__dict__
    for key in _object:
        aux_dict[key.split('__')[1]] = _object[key]
    return aux_dict

def translate_errors(field):
    translate_dict = {'country': "País", 'state': 'Estado', 'city': 'Cidade', 'street': 'Rua',
                      'company_name': 'Razão social',
                      'address_number': 'Número do endereço', 'name': 'Nome', 'birth_date': 'Nascimento',
                      'phone_number': 'Telefone', 'location': 'Localização', 'date': 'Data', 'cep': 'CEP', 'cpf': 'CPF'}
    if field in translate_dict.keys():
        return translate_dict[field]
    else:
        return field


def handle_exception(e):
    if isinstance(e, TypeError) or isinstance(e, ValueError):
        if 'is empty' in str(e):
            empty_field = str(e).split("'")[1]
            return f"O campo {translate_errors(empty_field)} deve ser preenchido!"
        elif 'Error with values of' in str(e):
            invalid_field = str(e).split("'")[1]
            return f"O campo {translate_errors(invalid_field)} é inválido!"
    else:
        return "Erro desconhecido!"