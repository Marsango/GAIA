import os

from PySide6.QtGui import QPixmap

from interface.base_windows.info_window import InfoDialog
from PySide6.QtWidgets import (QDialog)

class InfoWindow(QDialog, InfoDialog):
    def __init__(self) -> None:
        super(InfoWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Informações')
        self.setWindowIcon(QPixmap(os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "interface",
            "images"
        ).replace("\\", "/") + "/logo_lab.png"))
        self.pushButton.clicked.connect(self.close)
