from typing import get_type_hints
from .utils import *


class Address:
    def __init__(self, cep: str, country: str, state: str, city: str, street: str, address_number: str) -> None:
        verify_type(get_type_hints(Address.__init__), locals())
        self.__cep: str | None = None
        self.verify_valid_cep(cep)
        self.__country: str = country
        self.__state: str = state
        self.__city: str = city
        self.__street: str = street
        self.__address_number: str = address_number

    def verify_valid_cep(self, cep: str) -> None:
        for digit in cep:
            if not digit.isnumeric():
                raise ValueError("Error with values of 'cep'")
        if len(cep) != 8:
            raise ValueError("Error with values of 'cep'")
        self.__cep = cep