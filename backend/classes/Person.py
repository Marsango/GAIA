from Requester import Requester
from datetime import date
from typing import get_type_hints
from utils import verify_type
from Address import Address


class Person(Requester):
    def __init__(self, phone_number: str, email: str, name: str, birth_date: date, cpf: str, address: Address) -> None:
        verify_type(get_type_hints(Person.__init__), locals())
        self.__name: str = name
        self.__birth_date: date = birth_date
        self.__cpf: str = cpf
        Requester.__init__(self, phone_number, email, address)
