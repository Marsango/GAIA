from base_windows.configuration_window import ConfigurationDialog
from backend.classes.Configuration import Configuration
from PySide6.QtWidgets import (QDialog)


class ConfigurationWindow(QDialog, ConfigurationDialog):
    def __init__(self) -> None:
        super(ConfigurationWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Fatores Variáveis')
        self.save_config.clicked.connect(self.save)

    def save(self) -> None:
        config: Configuration = Configuration(float(self.phosphorum_factor.text()), float(self.potassium_factor.text()))
        config.save_config()
        self.close()

    def load(self) -> None:
        try:
            config: Configuration = Configuration()
            self.phosphorum_factor.insert(str(config.get_phosphor_factor()))
            self.potassium_factor.insert(str(config.get_potassium_factor()))
        except:
            return