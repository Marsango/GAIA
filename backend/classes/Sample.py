import math
from typing import get_type_hints
from backend.classes.Configuration import Configuration
from backend.classes.utils import verify_type
from interface.AlertWindow import AlertWindow
from interface.ConfigurationWindow import ConfigurationWindow
from datetime import datetime
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
                 copper: float, iron: float, manganese: float, zinc: float, silte: float, sand: float, clay: float) -> None:
        verify_type(get_type_hints(Sample.__init__), locals())
        try:
            current_config: Configuration = Configuration()
        except:
            dialog_message: AlertWindow = AlertWindow("Os fatores variáveis precisam ser configurados.")
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
        self.__phosphorus: float | None = phosphorus * current_config.get_phosphor_factor() if phosphorus is not None else None
        self.__potassium: float | None = potassium * current_config.get_phosphor_factor() if potassium is not None else None
        self.__organic_matter: float = organic_matter * 1.724 if organic_matter is not None else None
        self.__ph: float | None = ph
        self.__smp: float | None = smp
        self.__aluminum : float | None = aluminum
        if self.__organic_matter > 50:
            self.__h_al: float = math.pow(2.7182, (6.9056 - (0.08824 * self.__smp))) if smp is not None else None
        else:
            try:
                self.__h_al: float = conversion_table[round(self.__smp, 1)] if smp is not None else None
            except KeyError:
                raise ValueError(f"Error with values of 'SMP'. No conversion found for {round(self.__smp, 1)}.")
        self.__calcium: float | None = calcium
        self.__magnesium: float | None = magnesium
        self.__copper: float | None = copper
        self.__iron: float | None = iron
        self.__manganese: float | None = manganese
        self.__zinc: float | None = zinc
        self.__base_sum: float = self.__manganese + self.__calcium + self.__potassium if self.__manganese is not None and self.__calcium is not None and self.__potassium is not None else None
        self.__ctc: float = self.__base_sum + self.__h_al if self.__base_sum is not None and self.__h_al is not None else None
        self.__v_percent: float = (100 * self.__base_sum)/self.__ctc if self.__base_sum is not None and self.__ctc is not None else None
        self.__aluminum_saturation: float = (100 * self.__aluminum) / (self.__base_sum + self.__aluminum) if self.__aluminum is not None and self.__base_sum is not None else None
        self.__effective_ctc: float = self.__ctc + self.__aluminum if self.__ctc is not None and self.__aluminum is not None else None
        self.__clay: float | None = clay
        self.__sand: float | None = sand
        self.__silte: float | None = silte
        self.__classification =  self.find_classification(round((              1 + 0.3591 * (
                    (-0.02128887 * self.__sand) +
                    (-0.01005814 * self.__silte) +
                    (-0.01901894 * self.__clay) +
                    (0.0001171219 * self.__sand * self.__silte) +
                    (0.0002073924 * self.__sand * self.__clay) +
                    (0.00006118707 * self.__silte * self.__clay) -
                    (0.000006373789 * self.__sand * self.__silte * self.__clay)
                )
            ) ** 2.78474 * 10, 2)) if self.__clay is not None and self.__sand is not None and self.__silte is not None else None
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

    def find_classification(self, value):
        if value < 0.33:
            return 'AD0'
        elif value < 0.46:
            return 'AD1'
        elif value < 0.61:
            return 'AD2'
        elif value < 0.8:
            return 'AD3'
        elif value < 1.06:
            return 'AD4'
        elif value < 1.4:
            return 'AD5'
        else:
            return 'AD6'