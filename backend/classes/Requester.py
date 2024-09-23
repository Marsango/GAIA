from .utils import verify_type
from typing import get_type_hints
from .Address import Address


class Requester:
    def __init__(self, phone_number: str, email: str, address: Address) -> None:
        verify_type(get_type_hints(Requester.__init__), locals())
        self.__phone_number: str | None = None
        self.__email: str | None = None
        self.verify_valid_email(email)
        self.verify_valid_phone_number(phone_number)
        self.__address: Address = address

    def verify_valid_email(self, email: str) -> str:
        if not '@' in email or not '.' in email:
            raise ValueError("Error with values of 'email'")
        self.__email = email

    def verify_valid_phone_number(self, phone_number: str) -> str:
        for digit in phone_number:
            if not digit.isdecimal():
                raise ValueError("Error with values of 'phone_number'")
        self.__phone_number = phone_number