import os

from PySide6.QtGui import QPixmap

from interface.base_windows.information_window import InformationWindowDialog
from PySide6.QtWidgets import (QDialog)


class InformationWindow(QDialog, InformationWindowDialog):
    def __init__(self) -> None:
        super(InformationWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Informações!')

        self.setWindowIcon(QPixmap(os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "interface",
            "images"
        ).replace("\\", "/") + "/GAIA_icon.png"))

        self.ok_button.clicked.connect(self.close)