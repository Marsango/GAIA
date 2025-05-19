from typing import get_type_hints

from backend.classes.exceptions import InconsistencyError
from backend.classes.utils import verify_type


class Property:
    def __init__(self, name: str, location: str, city: str, state: str, country: str, registration_number: str) -> None:
        verify_type(get_type_hints(Property.__init__), locals())
        self.__name: str = name
        self.__location: str = location
        self.__country: str = country
        self.__state: str = state
        self.__city: str = city
        self.__registration_number: str | None = None
        self.verify_registration_number(registration_number)
        self.verify_valid_address(country, state, city)

    def verify_valid_address(self, country, state, city):
        """This functions verifies if the address is valid. By valid i mean, there no 'son' element with a null father
        Example, a country null cant have a state.
        Its calculated by the formula:
        if list is empty is valid
        if first element is 1, the len(3), len(3) - 1 = 2
        if first element is 2, the len(2), len(2) - 2 = 0
        if first element is 3, the len(1), len(1) - 3 = -2,
        So the idea is, if the address is valid, must satisfy the formula: len(null) - null[0] == 7 - 2*null[0]"""

        is_null: list[int] = []
        if country == '':
            is_null.append(1)
        if state == '':
            is_null.append(2)
        if city == '':
            is_null.append(3)
        if not is_null:
            return
        if len(is_null) - is_null[0] != 4 - 2*is_null[0]:
            raise InconsistencyError("Erro de consistência no endereço. Campos não podem ter 'pais' inválidos.")

    def get_location(self) -> dict[str, str]:
        return {"country": self.__country, "state": self.__state, "city": self.__city, "location": self.__location}

    def verify_registration_number(self, registration_number) -> None:
        if registration_number != '':
            try:
                int(registration_number)
            except:
                raise ValueError("Error with values of 'registration_number'")
            if int(registration_number) >= 0:
                self.__registration_number = registration_number
            else:
                raise ValueError("Error with values of 'registration_number'")
        else:
            self.__registration_number = None