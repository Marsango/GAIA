import sys
import os

from PySide6.QtGui import QPixmap
from PySide6.QtSvgWidgets import *
from PySide6.QtWidgets import (QApplication, QMainWindow)
from interface.GetReport import GetReport
from interface.InfoWindow import InfoWindow
from interface.base_windows.main_window import Ui_MainWindow
from interface.RequesterWindow import RequesterWindow
from interface.ConfigurationWindow import ConfigurationWindow
from interface.UploadLogo import UploadLogo
from interface.BackupWindow import BackupWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('GAIA SOFTWARE')
        self.showMaximized()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        bg_dir = os.path.join(base_dir, 'images/background.svg')
        self.setWindowIcon(QPixmap(os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "interface",
            "images"
        ).replace("\\", "/") + "/logo_lab.png"))
        self.svg_widget = QSvgWidget(bg_dir)
        self.horizontalLayout.addWidget(self.svg_widget)
        self.actionSolicitantes.triggered.connect(self.open_requester_window)
        self.actionFatores_vari_veis.triggered.connect(self.open_config_window)
        self.actionSobre.triggered.connect(self.open_info_window)
        self.actionConsultar_laudo_2.triggered.connect(self.open_get_report_window)
        self.actionLogo.triggered.connect(self.open_upload_logo_window)
        self.actionBackup.triggered.connect(self.open_backup_window)

    def open_requester_window(self) -> None:
        dialog: RequesterWindow = RequesterWindow()
        dialog.exec()

    def open_config_window(self) -> None:
        dialog: ConfigurationWindow = ConfigurationWindow()
        dialog.load()
        dialog.exec()

    def open_info_window(self) -> None:
        dialog: InfoWindow = InfoWindow()
        dialog.exec()

    def open_get_report_window(self) -> None:
        dialog: GetReport = GetReport()
        dialog.exec()

    def open_upload_logo_window(self) -> None:
        dialog: UploadLogo = UploadLogo()
        dialog.exec()

    def open_backup_window(self) -> None:
        dialog: BackupWindow = BackupWindow()
        dialog.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
