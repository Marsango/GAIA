from typing import get_type_hints
from utils import verify_type


class Sample:
    def __init__(self, name_description: str, total_area: float, collection_depth: float, phosphorus: float,
                 potassium: float,
                 organic_matter: float, pH: float, SMP: float, aluminum: float, H_Al: float, calcium: float,
                 magnesium: float,
                 copper: float, iron: float, manganese: float, zinc: float, base_saturation: float, cec: float,
                 v: float,
                 aluminum_saturation: float, effective_cec: float) -> None:
        verify_type(get_type_hints(Sample.__init__), locals())
        self.__name_description: str = name_description
        self.__total_area: float = total_area
        self.__collection_depth: float = collection_depth
        self.__phosphorus: float = phosphorus
        self.__potassium: float = potassium
        self.__organic_matter: float = organic_matter
        self.__pH: float = pH
        self.__SMP: float = SMP
        self.__aluminum: float = aluminum
        self.__H_Al: float = H_Al
        self.__calcium: float = calcium
        self.__magnesium: float = magnesium
        self.__copper: float = copper
        self.__iron: float = iron
        self.__manganese: float = manganese
        self.__zinc: float = zinc
        self.__base_saturation: float = base_saturation
        self.__CEC: float = cec
        self.__v: float = v
        self.__aluminum_saturation: float = aluminum_saturation
        self.__effective_CEC: float = effective_cec
