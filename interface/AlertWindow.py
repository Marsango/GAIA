from interface.base_windows.alert_window import AlertDialog
from PySide6.QtWidgets import (QDialog)


class AlertWindow(QDialog, AlertDialog):
    def __init__(self, message) -> None:
        super(AlertWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Alerta!')
        self.label_2.setText(message)
        self.pushButton.clicked.connect(self.close)