from .Requester import Requester
from datetime import date
from typing import get_type_hints, Any
from .utils import verify_type
from .Address import Address
from datetime import datetime


class Person(Requester):
    def __init__(self, phone_number: str, email: str, name: str, birth_date: str, cpf: str, address: Address) -> None:
        self.__birth_date: date | None = None
        verify_type(get_type_hints(Person.__init__), locals())
        self.verify_valid_date(birth_date)
        self.__name: str = name
        self.__cpf: str = cpf
        Requester.__init__(self, phone_number, email, address)

    def verify_valid_date(self, birth_date: str):
        try:
            self.__birth_date: date = datetime.strptime(birth_date, '%d/%m/%Y')
        except:
            raise ValueError("Error with values of 'birth_date'")
