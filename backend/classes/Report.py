from typing import get_type_hints
from utils import verify_type


class Report:
    def __init__(self, file_location: str) -> None:
        verify_type(get_type_hints(Report.__init__), locals())
        self.__file_location: str = file_location
