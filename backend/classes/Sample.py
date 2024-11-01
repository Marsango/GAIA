import math
from typing import get_type_hints
from backend.classes.Configuration import Configuration
from backend.classes.utils import verify_type
from interface.SucessfulRegister import SucessfulRegister
from interface.ConfigurationWindow import ConfigurationWindow
from datetime import datetime
from datetime import date
conversion_table = {
    3.5: 31.92, 3.6: 29.63, 3.7: 27.5, 3.8: 25.53, 3.9: 23.7, 4.0: 22.0,
    4.1: 20.42, 4.2: 18.96, 4.3: 17.6, 4.4: 16.33, 4.5: 15.16, 4.6: 14.08,
    4.7: 13.06, 4.8: 12.13, 4.9: 11.26, 5.0: 10.45, 5.1: 9.7, 5.2: 9.0,
    5.3: 8.36, 5.4: 7.76, 5.5: 7.2, 5.6: 6.69, 5.7: 6.21, 5.8: 5.76,
    5.9: 5.35, 6.0: 4.96, 6.1: 4.61, 6.2: 4.28, 6.3: 3.97, 6.4: 3.68,
    6.5: 3.42, 6.6: 3.18, 6.7: 2.95, 6.8: 2.74, 6.9: 2.54, 7.0: 2.36,
    7.1: 2.19, 7.2: 2.03, 7.3: 1.89, 7.4: 1.62, 7.6: 1.51, 7.7: 1.4,
    7.8: 1.3, 7.9: 1.21, 8.0: 1.12
}


class Sample:
    def __init__(self, description: str, total_area: float, depth: float, collection_date: str,
                 latitude: float, longitude: float, phosphorus: float,
                 potassium: float,
                 organic_matter: float, ph: float, smp: float, aluminum: float, calcium: float,
                 magnesium: float,
                 copper: float, iron: float, manganese: float, zinc: float) -> None:
        verify_type(get_type_hints(Sample.__init__), locals())
        try:
            current_config: Configuration = Configuration()
        except:
            dialog_message: SucessfulRegister = SucessfulRegister(sucess_message="Os fatores variáveis precisam ser configurados.")
            dialog_message.exec()
            dialog_config: ConfigurationWindow = ConfigurationWindow()
            dialog_config.exec()
            current_config: Configuration = Configuration()
        self.__description: str = description
        self.__total_area: float = total_area
        self.__depth: float = depth
        self.__collection_date: str | None = None
        self.__longitude: float | None = None
        self.__latitude: float | None = None
        self.__phosphorus: float = phosphorus * current_config.get_phosphor_factor()
        self.__potassium: float = potassium * current_config.get_phosphor_factor()
        self.__organic_matter: float = organic_matter * 1.724
        self.__ph: float = ph
        self.__smp: float = smp
        self.__aluminum: float = aluminum
        if self.__organic_matter > 50:
            self.__h_al: float = math.pow(2.7182, (6.9056 - (0.08824 * self.__smp)))
        else:
            try:
                self.__h_al: float = conversion_table[round(self.__smp, 1)]
            except KeyError:
                raise ValueError(f"Error with values of 'SMP'. No conversion found for {round(self.__smp, 1)}.") #raise ValueError("Error with values of 'SMP'")
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
        self.verify_valid_latitude(latitude)
        self.verify_valid_longitude(longitude)


    def verify_valid_date(self, collection_date: str) -> None:
        try:
            self.__collection_date: str = datetime.strptime(collection_date, '%d/%m/%Y').strftime("%d/%m/%Y")
        except:
            raise ValueError("Error with values of 'Data'")

    def verify_valid_latitude(self, latitude: float) -> None:
        if -90 <= latitude <= 90:
            self.__latitude: float = latitude
        else:
            raise ValueError("Error with values of 'latitude'")

    def verify_valid_longitude(self, longitude: float) -> None:
        if -180 <= longitude <= 180:
            self.__longitude: float = longitude
        else:
            raise ValueError("Error with values of 'longitude'")

