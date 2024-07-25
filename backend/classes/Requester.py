from .utils import verify_type
from typing import get_type_hints
from .Address import Address


class Requester:
    def __init__(self, phone_number: str, email: str, address: Address) -> None:
        verify_type(get_type_hints(Requester.__init__), locals())
        self.__phone_number: str = phone_number
        self.__email: str = email
        self.__address: Address = address
