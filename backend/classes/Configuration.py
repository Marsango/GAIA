import json
from backend.classes.utils import verify_type
from typing import get_type_hints, Any
import os


class Configuration:

    def __init__(self, **kwargs) -> None:
        verify_type(get_type_hints(Configuration.__init__), locals())
        base_dir: str = os.path.dirname(os.path.abspath(__file__))
        self.__file_location = os.path.join(base_dir, 'config.json')
        self.__user_config = kwargs.get('selected_config')
        if self.__user_config is not None:
            self.save_config()
        self.__current_config = self.load_config()

    def save_config(self) -> None:
        if os.path.isfile(self.__file_location):
            with open(self.__file_location, "r") as current_file:
                current_data: dict = json.load(current_file)
            for element in self.__user_config.keys():
                current_data['current_selection'][element] = self.__user_config[element]['selected']
                current_data[self.__user_config[element]['selected']][element] = self.__user_config[element]['value']
            with open(self.__file_location, "w") as current_file:
                json.dump(current_data, current_file)
        else:
            new_data: dict[str, dict[str, float | None]] = {'current_selection': {'phosphorus': None,
                                                                             'potassium': None,
                                                                             'organic_matter': None},
                                                       'factors': {'phosphorus': None,
                                                                   'potassium': None,
                                                                   'organic_matter': None},
                                                       'line_equation': {
                                                           'phosphorus': {'a': None, 'b': None},
                                                           'potassium': {'a': None, 'b': None},
                                                           'organic_matter': {'a': None, 'b': None}
                                                       }}
            for element in self.__user_config.keys():
                new_data['current_selection'][element] = self.__user_config[element]['selected']
                new_data[self.__user_config[element]['selected']][element] = self.__user_config[element]['value']
            with open(self.__file_location, "w") as new_file:
                json.dump(new_data, new_file)

    def get_phosphorus_correction(self) -> float | None:
        return self.__current_config['phosphorus']['value']

    def get_potassium_correction(self) -> float | None:
        return self.__current_config['potassium']['value']

    def get_organic_matter_correction(self) -> float | None:
        return self.__current_config['organic_matter']['value']

    def get_current_config(self) -> dict[str, dict[str, str | float | None | dict]]:
        return self.__current_config

    def load_config(self) -> dict[str, dict[str, str | float | None | dict]]:
        if os.path.isfile(self.__file_location):
            with open(self.__file_location, "r") as file:
                saved_config: dict[Any] = json.load(file)

            return {
                'phosphorus':
                    {'selected': saved_config['current_selection']['phosphorus'],
                     'value': saved_config['factors']['phosphorus'] if saved_config['current_selection']['phosphorus']
                                                                       == 'factors' else saved_config['line_equation'][
                         'phosphorus']
                     },
                'potassium':
                    {'selected': saved_config['current_selection']['potassium'],
                     'value': saved_config['factors']['potassium'] if saved_config['current_selection']['potassium']
                                                                      == 'factors' else saved_config['line_equation'][
                         'potassium']
                     },
                'organic_matter':
                    {'selected': saved_config['current_selection']['organic_matter'],
                     'value': saved_config['factors']['organic_matter'] if saved_config['current_selection'][
                                                                               'organic_matter']
                                                                           == 'factors' else
                     saved_config['line_equation'][
                         'organic_matter']
                     }
            }
        else:
            raise FileNotFoundError('Configuration file not found.')

    def get_current_json(self) -> dict[str, dict[float | None]]:
        if os.path.isfile(self.__file_location):
            with open(self.__file_location, "r") as file:
                current_file: dict[Any] = json.load(file)
            return current_file
        else:
            raise FileNotFoundError('Configuration file not found.')
