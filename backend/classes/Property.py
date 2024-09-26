from typing import get_type_hints
from backend.classes.utils import verify_type


class Property:
    def __init__(self, name: str, location: str, city: str, state: str, country: str, registration_number: str) -> None:
        verify_type(get_type_hints(Property.__init__), locals())
        self.__name: str = name
        self.__location: str = location
        self.__country: str = country
        self.__state: str = state
        self.__city: str = city
        self.__registration_number: str = registration_number

    def get_location(self) -> dict[str, str]:
        return {"country": self.__country, "state": self.__state, "city": self.__city, "location": self.__location}
