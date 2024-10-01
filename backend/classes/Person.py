from backend.classes.Requester import Requester
from datetime import date
from typing import get_type_hints, Any
from backend.classes.utils import verify_type
from backend.classes.Address import Address
from datetime import datetime


class Person(Requester):
    def __init__(self, phone_number: str, email: str, name: str, birth_date: str, cpf: str, address: Address) -> None:
        self.__birth_date: date | None = None
        self.__cpf: str | None = None
        verify_type(get_type_hints(Person.__init__), locals())
        self.verify_valid_date(birth_date)
        self.verify_valid_cpf(cpf)
        self.__name: str | None = None
        self.verify_name(name)
        Requester.__init__(self, phone_number, email, address)

    def verify_valid_date(self, birth_date: str) -> None:
        try:
            self.__birth_date: str = datetime.strptime(birth_date, '%d/%m/%Y').strftime("%d/%m/%Y")
        except:
            raise ValueError("Error with values of 'birth_date'")

    def verify_valid_cpf(self, cpf: str) -> None:
        if len(cpf) != 11:
            raise ValueError("Error with values of 'cpf'")
        equal_numbers: list[str] = [x for x in cpf if x == cpf[0]]
        if len(equal_numbers) == 11:
            raise ValueError("Error with values of 'cpf'")
        first_digit_verification: int = int(cpf[-2])
        second_digit_verification: int = int(cpf[-1])

        def verify_valid_digit(expected_digit, cpf_fraction) -> None:
            digit_sum: int = sum([int(x)*(len(cpf_fraction) + 1 - i) for i, x in enumerate(cpf_fraction)])
            calculated_digit: int = (digit_sum * 10 % 11) % 10
            if int(expected_digit) != calculated_digit:
                raise ValueError("Error with values of 'cpf'")

        verify_valid_digit(first_digit_verification, cpf[:9])
        verify_valid_digit(second_digit_verification, cpf[:10])
        self.__cpf: str = cpf

    def verify_name(self, name: str):
        if any(char.isdigit() for char in name):
            raise ValueError("Error with values of 'cpf'")
        self.__name = name