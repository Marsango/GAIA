import json
import logging
from typing import Any
from .exceptions import CPFAlreadyExistsError


def read_current_stored_config() -> dict[str, float]:
    try:
        with open("config.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        logging.error("Arquivo de configuração não encontrado.")
        raise FileNotFoundError("O arquivo de configuração 'config.json' não foi encontrado.")
    except json.JSONDecodeError as e:
        logging.error(f"Erro ao ler o arquivo de configuração: {e}")
        raise ValueError("Erro ao processar o arquivo de configuração.")


def verify_type(type_hints: dict[str, Any], function_parameters: dict[str, Any]) -> None:
    for key in type_hints:
        if key == 'return':
            continue
        if key not in function_parameters:
            logging.error(f"Parâmetro ausente: {key}")
            raise TypeError(f"O parâmetro '{key}' está ausente.")
        if not isinstance(function_parameters[key], type_hints[key]):
            logging.error(f"Erro de tipo para '{key}': Esperado {type_hints[key]}, mas foi recebido {type(function_parameters[key])}.")
            raise TypeError(f"Erro de tipo no campo '{key}': Esperado {type_hints[key]}, mas foi recebido {type(function_parameters[key])}.")
        if isinstance(function_parameters[key], str):
            if function_parameters[key] == '':
                logging.warning(f"Campo vazio detectado para '{key}'.")
                raise ValueError(f"O campo '{translate_errors(key)}' não pode ser vazio.")


def to_dict(_object: Any) -> dict[str, Any]:
    try:
        aux_dict: dict[str, Any] = {}
        _object = _object.__dict__
        for key in _object:
            aux_dict[key.split('__')[1]] = _object[key]
        return aux_dict
    except Exception as e:
        logging.error(f"Erro ao converter objeto para dicionário: {e}")
        raise ValueError("Erro ao converter objeto para dicionário.")


def translate_errors(field: str) -> str:
    translate_dict = {'country': "País", 'state': 'Estado', 'city': 'Cidade', 'street': 'Rua',
                      'company_name': 'Razão social',
                      'address_number': 'Número do endereço', 'name': 'Nome', 'birth_date': 'Nascimento',
                      'phone_number': 'Telefone', 'location': 'Localização', 'date': 'Data', 'cep': 'CEP', 'cpf': 'CPF'}
    return translate_dict.get(field, field)


def handle_exception(e: Exception) -> str:
    # Verifica se é um erro de tipo ou valor
    if isinstance(e, TypeError) or isinstance(e, ValueError):
        if 'is empty' in str(e):
            empty_field = str(e).split("'")[1]
            error_message = f"O campo '{translate_errors(empty_field)}' deve ser preenchido corretamente!"
            logging.warning(error_message)
            return error_message
        elif 'Error with values of' in str(e):
            invalid_field = str(e).split("'")[1]
            error_message = f"O campo '{translate_errors(invalid_field)}' possui valores inválidos!"
            logging.warning(error_message)
            return error_message
        elif 'CPF inválido' in str(e):
            return str(e)
        else:
            return f'Erro desconhecido: {str(e)}'

    # Verifica se é um erro de CPF duplicado
    elif isinstance(e, CPFAlreadyExistsError):
        error_message = f"Erro de CPF: {str(e)}"
        logging.error(error_message)
        return error_message

    # Outros tipos de erro
    else:
        error_message = f"Erro desconhecido: {str(e)}"
        logging.error(error_message)
        return "Ocorreu um erro desconhecido. Por favor, tente novamente mais tarde."

