from PIL.ImageQt import QPixmap

from interface.base_windows.backup_window import BackupDialog
from interface.AlertWindow import AlertWindow
from backend.classes.Database import Database
from PySide6.QtWidgets import (QDialog, QFileDialog)
import shutil, os
import datetime


class BackupWindow(QDialog, BackupDialog):
    def __init__(self) -> None:
        super(BackupWindow, self).__init__()
        self.setupUi(self)
        self.__db_location = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "backend",
            "classes"
        ).replace("\\", "/") + "/soil_analysis.db"
        self.__report_location = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "reports"
        ).replace("\\", "/")
        self.setWindowTitle('Opções de backup')
        self.setWindowIcon(QPixmap(os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "interface",
            "images"
        ).replace("\\", "/") + "/logo_lab.png"))
        db: Database = Database()
        self.requester_count.setText(str(len(db.get_requesters())))
        self.property_count.setText(str(len(db.get_properties())))
        self.sample_count.setText(str(len(db.get_samples())))
        self.select_folder.clicked.connect(self.open_dialog)
        self.backup_button.clicked.connect(self.backup)

    def open_dialog(self) -> None:
        filename: QFileDialog.getOpenFileName = QFileDialog.getExistingDirectory()
        self.backup_path.setText(filename)

    def backup(self) -> None:
        shutil.copy(self.__db_location, f"{self.backup_path.text()}/backup_gaia_{str(datetime.datetime.now()).split('.')[0].replace(' ', '_').replace(':', '-')}.db")
        if self.backup_checkbox.isChecked():
            shutil.copytree(self.__report_location, self.backup_path.text(), dirs_exist_ok=True)
        dialog: AlertWindow = AlertWindow("Backup salvo com sucesso!")
        dialog.exec()

