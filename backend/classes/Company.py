from .Requester import Requester
from typing import get_type_hints
from .utils import verify_type
from .Address import Address


class Company(Requester):
    def __init__(self, phone_number: str, email: str, company_name: str, cnpj: str,
                 address: Address) -> None:
        verify_type(get_type_hints(Company.__init__), locals())
        self.__company_name: str = company_name
        self.__cnpj: str | None = None
        self.verify_cnpj(cnpj)
        Requester.__init__(self, phone_number, email, address)


    def get_cnpj_verificator(self, cnpj_part: str) -> int:
        weights_list = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        if len(cnpj_part) == 12:
            weights_list = weights_list[1:]
        sum_verificator = sum([weights_list[i] * int(x) for i, x in enumerate(cnpj_part)]) % 11
        if sum_verificator == 0 or sum_verificator == 1:
            return 0
        else:
            return 11 - sum_verificator


    def verify_cnpj(self, cnpj: str) -> None:
        _sum: int = 0
        if len(cnpj) != 14 or any(not char.isdigit() for char in cnpj):
            raise ValueError("Error with values of 'cnpj'")
        sum_verificator_one = self.get_cnpj_verificator(cnpj[:-2])
        sum_verificator_two = self.get_cnpj_verificator(cnpj[:-1])
        if sum_verificator_one != int(cnpj[-2]) or sum_verificator_two != int(cnpj[-1]):
            raise ValueError(f"Error with values of 'cnpj'")
        self.__cnpj = cnpj