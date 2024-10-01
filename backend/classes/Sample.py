from typing import get_type_hints
from backend.classes.utils import verify_type
from datetime import datetime
from datetime import date

class Sample:
    def __init__(self, description: str, total_area: float, depth: float, collection_date: str,
                 latitude: float, longitude: float, phosphorus: float,
                 potassium: float,
                 organic_matter: float, ph: float, smp: float, aluminum: float, h_al: float, calcium: float,
                 magnesium: float,
                 copper: float, iron: float, manganese: float, zinc: float) -> None:
        verify_type(get_type_hints(Sample.__init__), locals())
        self.__description: str = description
        self.__total_area: float = total_area
        self.__depth: float = depth
        self.__collection_date: str | None = collection_date
        self.__latitude: float = latitude
        self.__longitude: float = longitude
        self.__phosphorus: float = phosphorus
        self.__potassium: float = potassium
        self.__organic_matter: float = organic_matter
        self.__ph: float = ph
        self.__smp: float = smp
        self.__aluminum: float = aluminum
        self.__h_al: float = h_al
        self.__calcium: float = calcium
        self.__magnesium: float = magnesium
        self.__copper: float = copper
        self.__iron: float = iron
        self.__manganese: float = manganese
        self.__zinc: float = zinc
        self.__base_sum: float = self.__manganese + self.__calcium + self.__potassium
        self.__ctc: float = self.__base_sum + self.__h_al
        self.__v_percent: float = (100 * self.__base_sum)/self.__ctc
        self.__aluminum_saturation: float = (100 * self.__aluminum) / (self.__base_sum + self.__aluminum)
        self.__effective_ctc: float = self.__ctc + self.__aluminum
        self.verify_valid_date(collection_date)


    def verify_valid_date(self, collection_date: str) -> None:
        try:
            self.__collection_date: str = datetime.strptime(collection_date, '%d/%m/%Y').strftime("%d/%m/%Y")
        except:
            raise ValueError("Error with values of 'birth_date'")