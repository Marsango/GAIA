import json
from backend.classes.utils import verify_type
from typing import get_type_hints
import os

class Configuration:

    def __init__(self, phosphor_factor: float | None = None, potassium_factor: float | None = None) -> None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_location = os.path.join(base_dir, 'config.json')
        if phosphor_factor is None or potassium_factor is None:
            with open(self.file_location, "r") as file:
                self.load_config(json.load(file))
            if self.__phosphor_factor is None or self.__potassium_factor is None:
                raise ValueError("Configuration file not found.")
            return
        verify_type(get_type_hints(Configuration.__init__), locals())
        self.__phosphor_factor: float | None = phosphor_factor
        self.__potassium_factor: float | None = potassium_factor

    def save_config(self) -> None:
        with open(self.file_location, "w") as file:
            json.dump({'phosphor_factor': self.__phosphor_factor, 'potassium_factor': self.__potassium_factor}, file)

    def set_phosphor_factor(self, phosphor_factor: float) -> None:
        verify_type(get_type_hints(Configuration.set_phosphor_factor), locals())
        self.__phosphor_factor = phosphor_factor

    def set_potassium_factor(self, potassium_factor: float) -> None:
        verify_type(get_type_hints(Configuration.set_potassium_factor), locals())
        self.__potassium_factor = potassium_factor

    def get_phosphor_factor(self) -> float:
        return self.__phosphor_factor

    def get_potassium_factor(self) -> float:
        return self.__potassium_factor

    def load_config(self, saved_config: dict[str, float]) -> None:
        self.__phosphor_factor = saved_config['phosphor_factor']
        self.__potassium_factor = saved_config['potassium_factor']

    def __repr__(self) -> str:
        return f'Phosphor factor: {self.__phosphor_factor}, Potassium_factor: {self.__potassium_factor} '
