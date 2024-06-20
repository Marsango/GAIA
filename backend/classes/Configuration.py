import json
from typing import Any


def read_current_stored_config() -> dict[str, float]:
    with open("config.json", "r") as file:
        return json.load(file)


def verify_type(variable: Any, type_variable: Any) -> bool:
    if isinstance(variable, type_variable):
        return True
    raise TypeError


class Configuration:

    def __init__(self, phosphor_factor: float | None = None, potassium_factor: float | None = None) -> None:
        if phosphor_factor is None and potassium_factor is None:
            self.__phosphor_factor: float | None = None
            self.__potassium_factor: float | None = None
            return
        if verify_type(phosphor_factor, float):
            self.__phosphor_factor: float | None = phosphor_factor
        if verify_type(potassium_factor, float):
            self.__potassium_factor: float | None = potassium_factor

    def save_config(self) -> None:
        with open("config.json", "w") as file:
            json.dump({'phosphor_factor': self.__phosphor_factor, 'potassium_factor': self.__potassium_factor}, file)

    def set_phosphor_factor(self, phosphor_factor: float) -> None:
        if verify_type(phosphor_factor, float):
            self.__phosphor_factor = phosphor_factor

    def set_potassium_factor(self, potassium_factor: float) -> None:
        if verify_type(potassium_factor, float):
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


