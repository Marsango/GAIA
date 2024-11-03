from interface.base_windows.info_window import InfoDialog
from PySide6.QtWidgets import (QDialog)

class InfoWindow(QDialog, InfoDialog):
    def __init__(self) -> None:
        super(InfoWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Informações')
        self.pushButton.clicked.connect(self.close)
