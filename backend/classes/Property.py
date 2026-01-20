from typing import get_type_hints
from backend.classes.utils import verify_type


class Property:
    def __init__(
        self,
        name: str,
        registration_number: str,
        localizacao: str = "",
    ) -> None:
        self.__name = name
        self.__registration_number = registration_number
        self.__localizacao = localizacao

    def get_name(self) -> str:
        return self.__name

    def get_registration_number(self) -> str:
        return self.__registration_number

    def get_localizacao(self) -> str:
        return self.__localizacao