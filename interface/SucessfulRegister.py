from interface.base_windows.sucessful_register import SucessfulDialog
from PySide6.QtWidgets import (QDialog)

class SucessfulRegister(QDialog, SucessfulDialog):
    def __init__(self, **kwargs) -> None:
        super(SucessfulRegister, self).__init__()
        self.setupUi(self)
        message: str = kwargs.get('sucess_message')
        if message:
            self.label.setText(f"<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">{message}</span></p></body></html>")
        self.pushButton.clicked.connect(self.close)
