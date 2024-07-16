from typing import get_type_hints
from utils import verify_type


class Property:
    def __init__(self, latitude: float, longitude: float, name: str, location: str) -> None:
        verify_type(get_type_hints(Property.__init__), locals())
        self.__latitude: float = latitude
        self.__longitude: float = longitude
        self.__name: str = name
        self.__location: str = location
