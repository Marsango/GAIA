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
        ).replace("\\", "/") + "/logo_lab.png"))
        self.save_config.clicked.connect(self.save)

    def save(self) -> None:
        try:
            config: Configuration = Configuration(float(self.phosphorum_factor.text()), float(self.potassium_factor.text()))
            config.save_config()
            dialog: AlertWindow = AlertWindow("Configurações salvas com sucesso!")
            dialog.exec()
            self.close()
        except:
            dialog: AlertWindow = AlertWindow("Por favor insira um número válido.")
            dialog.exec()
            self.load()

    def load(self) -> None:
        try:
            config: Configuration = Configuration()
            self.phosphorum_factor.setText(str(config.get_phosphor_factor()))
            self.potassium_factor.setText(str(config.get_potassium_factor()))
        except:
            return