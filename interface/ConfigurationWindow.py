import os

from PySide6.QtGui import QPixmap

from interface.base_windows.configuration_window import ConfigurationDialog
from backend.classes.Configuration import Configuration
from PySide6.QtWidgets import (QDialog)
from interface.AlertWindow import AlertWindow


class ConfigurationWindow(QDialog, ConfigurationDialog):
    def __init__(self) -> None:
        super(ConfigurationWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Fatores Variáveis')
        self.setWindowIcon(QPixmap(os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "interface",
            "images"
        ).replace("\\", "/") + "/GAIA_icon.png"))
        self.save_config.clicked.connect(self.save)
        self.phosphorus_widget_line.hide()
        self.phosphorus_widget_factor.show()
        self.potassium_widget_line.hide()
        self.potassium_widget_factor.show()
        self.organic_matter_widget_line.hide()
        self.organic_matter_widget_factor.show()
        self.setMaximumSize(448, 377)
        self.phosphorus_combobox.currentIndexChanged.connect(self.change_window)
        self.potassium_combobox.currentIndexChanged.connect(self.change_window)
        self.organic_matter_combobox.currentIndexChanged.connect(self.change_window)
        self.load()

    def save(self) -> None:
        try:
            current_selection: dict[str, str] = {'phosphorus': 'factors' if self.phosphorus_combobox.currentIndex() == 0 else 'line_equation',
                                      'potassium': 'factors' if self.potassium_combobox.currentIndex() == 0 else 'line_equation',
                                      'organic_matter': 'factors' if self.organic_matter_combobox.currentIndex() == 0 else 'line_equation'}

            factors: dict[str, float | None] = {'phosphorus': float(self.phosphorus_factor.text()) if self.phosphorus_factor.text() != '' else None,
                            'potassium': float(self.potassium_factor.text()) if self.potassium_factor.text() != '' else None,
                            'organic_matter': float(self.organic_matter_factor.text()) if self.organic_matter_factor.text() != '' else None}

            line_equation: dict[str, dict[str, float | None]] = {'phosphorus': {'a': float(self.phosphorus_a.text()) if self.phosphorus_a.text() != '' else None,
                                                 'b': float(self.phosphorus_b.text()) if self.phosphorus_b.text() != '' else None},
                                  'potassium': {'a': float(self.potassium_a.text()) if self.potassium_a.text() != '' else None,
                                                 'b': float(self.potassium_b.text()) if self.potassium_b.text() != '' else None},
                                  'organic_matter': {'a': float(self.organic_matter_a.text()) if self.organic_matter_a.text() != '' else None,
                                                 'b': float(self.organic_matter_b.text()) if self.organic_matter_b.text() != '' else None}}

            selected_config: dict[str, dict[str, str | float | None | dict]] = {
                'phosphorus':
                    {'selected': current_selection['phosphorus'],
                    'value': factors['phosphorus'] if current_selection['phosphorus'] == 'factors' else line_equation['phosphorus']
                     },
                'potassium':
                    {'selected': current_selection['potassium'],
                    'value': factors['potassium'] if current_selection['potassium'] == 'factors' else line_equation['potassium']
                     },
                'organic_matter':
                    {'selected': current_selection['organic_matter'],
                    'value': factors['organic_matter'] if current_selection['organic_matter'] == 'factors' else line_equation['organic_matter']
                     }
            }
            for element in selected_config.keys():
                if not isinstance(selected_config[element]['value'], dict):
                    if selected_config[element]['value'] is None:
                        raise TypeError('Todos os valores devem ser preenchidos.')
                else:
                    if selected_config[element]['value']['a'] is None or selected_config[element]['value']['b'] is None:
                        raise TypeError('Todos os valores devem ser preenchidos.')
            config: Configuration = Configuration(selected_config=selected_config)
            config.save_config()
            dialog: AlertWindow = AlertWindow("Configurações salvas com sucesso!")
            dialog.exec()
            self.close()
        except ValueError as e:
            dialog: AlertWindow = AlertWindow(str(e))
            dialog.exec()
            self.load()
        except TypeError as e:
            dialog: AlertWindow = AlertWindow(str(e))
            dialog.exec()

    def load(self) -> None:
        try:
            index_relation: list = ['factors', 'line_equation']
            config: Configuration = Configuration()
            current_file: dict = config.get_current_json()
            self.phosphorus_combobox.setCurrentIndex(index_relation.index(current_file['current_selection']['phosphorus']))
            self.potassium_combobox.setCurrentIndex(index_relation.index(current_file['current_selection']['potassium']))
            self.organic_matter_combobox.setCurrentIndex(index_relation.index(current_file['current_selection']['organic_matter']))
            self.phosphorus_factor.setText(
                str(current_file['factors']['phosphorus']) if current_file['factors']['phosphorus'] is not None else '')
            self.potassium_factor.setText(
                str(current_file['factors']['potassium']) if current_file['factors']['potassium'] is not None else '')
            self.organic_matter_factor.setText(
                str(current_file['factors']['organic_matter']) if current_file['factors'][
                                                                      'organic_matter'] is not None else '')
            self.phosphorus_a.setText(
                str(current_file['line_equation']['phosphorus']['a']) if current_file['line_equation']['phosphorus'][
                                                                             'a'] is not None else '')
            self.potassium_a.setText(
                str(current_file['line_equation']['potassium']['a']) if current_file['line_equation']['potassium'][
                                                                            'a'] is not None else '')
            self.organic_matter_a.setText(str(current_file['line_equation']['organic_matter']['a']) if
                                          current_file['line_equation']['organic_matter']['a'] is not None else '')
            self.phosphorus_b.setText(
                str(current_file['line_equation']['phosphorus']['b']) if current_file['line_equation']['phosphorus'][
                                                                             'b'] is not None else '')
            self.potassium_b.setText(
                str(current_file['line_equation']['potassium']['b']) if current_file['line_equation']['potassium'][
                                                                            'b'] is not None else '')
            self.organic_matter_b.setText(str(current_file['line_equation']['organic_matter']['b']) if
                                          current_file['line_equation']['organic_matter']['b'] is not None else '')

        except:
            return

    def change_window(self) -> None:
        sender = self.sender()
        if sender == self.phosphorus_combobox:
            if self.phosphorus_combobox.currentIndex() == 0:
                self.phosphorus_widget_line.hide()
                self.phosphorus_widget_factor.show()
            else:
                self.phosphorus_widget_factor.hide()
                self.phosphorus_widget_line.show()
        elif sender == self.potassium_combobox:
            if self.potassium_combobox.currentIndex() == 0:
                self.potassium_widget_line.hide()
                self.potassium_widget_factor.show()
            else:
                self.potassium_widget_factor.hide()
                self.potassium_widget_line.show()
        elif sender == self.organic_matter_combobox:
            if self.organic_matter_combobox.currentIndex() == 0:
                self.organic_matter_widget_line.hide()
                self.organic_matter_widget_factor.show()
            else:
                self.organic_matter_widget_factor.hide()
                self.organic_matter_widget_line.show()
