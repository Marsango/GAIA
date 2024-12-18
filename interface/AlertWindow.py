import os

from PySide6.QtGui import QPixmap

from interface.base_windows.alert_window import AlertDialog
from PySide6.QtWidgets import (QDialog)


class AlertWindow(QDialog, AlertDialog):
    def __init__(self, message) -> None:
        super(AlertWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Alerta!')
        self.setWindowIcon(QPixmap(os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "interface",
            "images"
        ).replace("\\", "/") + "/logo_lab.png"))
        self.label_2.setText(message)
        self.pushButton.clicked.connect(self.close)