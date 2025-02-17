from interface.base_windows.upload_logo import UploadLogoDialog
from interface.AlertWindow import AlertWindow
from PySide6.QtWidgets import (QDialog, QFileDialog)
from PySide6.QtGui import (QPixmap)
import shutil, os


class UploadReportStamp(QDialog, UploadLogoDialog):
    def __init__(self) -> None:
        super(UploadReportStamp, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Atualizar selo")
        self.setWindowIcon(QPixmap(os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "interface",
            "images"
        ).replace("\\", "/") + "/GAIA_icon.png"))
        self.instruction.setText("ATENÇÃO! A imagem do selo não deve ter fundo ou vai sobrepor outros elementos do laudo.")
        self.file_path.setReadOnly(True)
        self.upload_button.clicked.connect(self.upload)
        self.save_button.clicked.connect(self.save)
        self.__image_location = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "interface",
            "images"
        ).replace("\\", "/")
        self.label_2.setText('Selo atual')
        self.image_label.setPixmap(QPixmap(f"{self.__image_location}/report_stamp.png"))

    def upload(self) -> None:
        filename: QFileDialog.getOpenFileName = QFileDialog.getOpenFileName()[0]
        self.file_path.setText(filename)
        self.image_label.setPixmap(QPixmap(filename))
        self.label_2.setText("Preview")

    def save(self) -> None:
        shutil.copy(self.file_path.text(), f"{self.__image_location}/report_stamp.png")
        dialog: AlertWindow = AlertWindow("Logo salva com sucesso!")
        dialog.exec()

