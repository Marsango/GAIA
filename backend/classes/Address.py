from typing import get_type_hints
from backend.classes.utils import *
from backend.classes.exceptions import InconsistencyError


class Address:
    def __init__(self, cep: str, country: str, state: str, city: str, street: str, address_number: str) -> None:
        verify_type(get_type_hints(Address.__init__), locals())
        self.verify_valid_address(country, state, city, street, address_number, cep)
        self.__cep: str | None = None
        self.verify_valid_cep(cep)
        self.__country: str | None = country
        self.__state: str | None = state
        self.__city: str | None = city
        self.__street: str | None = street
        self.__address_number: str | None = address_number

    def verify_valid_cep(self, cep: str) -> None:
        if cep == '':
            self.__cep = cep
            return
        for digit in cep:
            if not digit.isnumeric():
                raise ValueError("Error with values of 'cep'")
        if len(cep) != 8:
            raise ValueError("Error with values of 'cep'")
        self.__cep = cep

    def verify_valid_address(self, country, state, city, street, address_number, cep):
        """This functions verifies if the address is valid. By valid i mean, there no 'son' element with a null father
        Example, a country null cant have a state.
        Its calculated by the formula:
        if list is empty is valid
        if first element is 1, the len(6), len(6) - 1 = 5
        if first element is 2, the len(5), len(5) - 2 = 3
        if first element is 3, the len(4), len(4) - 3 = 1,
        So the idea is, if the address is valid, must satisfy the formula: len(null) - null[0] == 7 - 2*null[0]"""

        is_null: list[int] = []
        if country == '':
            is_null.append(1)
        if state == '':
            is_null.append(2)
        if city == '':
            is_null.append(3)
        if street == '':
            is_null.append(4)
        if address_number == '':
            is_null.append(5)
        if cep == '':
            is_null.append(6)
        if not is_null:
            return
        if len(is_null) - is_null[0] != 7 - 2*is_null[0]:
            raise InconsistencyError("Erro de consistência no endereço. Campos não podem ter 'pais' inválidos.")