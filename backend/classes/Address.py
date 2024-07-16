from typing import get_type_hints
from utils import verify_type


class Address:
    def __init__(self, cep: str, country: str, state: str, city: str, street: str, number: int) -> None:
        verify_type(get_type_hints(Address.__init__), locals())
        self.__CEP: str = cep
        self.__country: str = country
        self.__state: str = state
        self.__city: str = city
        self.__street: str = street
        self.__number: int = number
