from base_windows.error_window import ErrorDialog
from PySide6.QtWidgets import (QDialog)


class ErrorWindow(QDialog, ErrorDialog):
    def __init__(self, error) -> None:
        super(ErrorWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Erro!')
        self.label_2.setText(error)
        self.pushButton.clicked.connect(self.close)