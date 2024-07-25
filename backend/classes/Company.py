from .Requester import Requester
from typing import get_type_hints
from .utils import verify_type
from .Address import Address


class Company(Requester):
    def __init__(self, phone_number: str, email: str, company_name: str, cnpj: str,
                 address: Address) -> None:
        verify_type(get_type_hints(Company.__init__), locals())
        self.__company_name: str = company_name
        self.__cnpj: str = cnpj
        Requester.__init__(self, phone_number, email, address)

