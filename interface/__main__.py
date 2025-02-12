import sys
import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtSvgWidgets import *
from PySide6.QtWidgets import (QApplication, QMainWindow)
from interface.GetReport import GetReport
from interface.InfoWindow import InfoWindow
from interface.base_windows.main_window import Ui_MainWindow
from interface.RequesterWindow import RequesterWindow
from interface.ConfigurationWindow import ConfigurationWindow
from interface.UploadLogo import UploadLogo
from interface.BackupWindow import BackupWindow
from interface.UploadReportStamp import UploadReportStamp
import ctypes
myappid = 'mycompany.myproduct.subproduct.version'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('GAIA SOFTWARE')
        self.showMaximized()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        bg_dir = os.path.join(base_dir, 'images', 'background.svg')
        self.setWindowIcon(QIcon(os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "interface",
            "images"
        ).replace("\\", "/") + "/GAIA_icon.ico"))
        self.svg_widget = QSvgWidget(bg_dir)
        self.horizontalLayout.addWidget(self.svg_widget)

        # Lista para rastrear janelas abertas
        self.open_windows = []

        # Conectar ações a métodos
        self.actionSolicitantes.triggered.connect(self.open_requester_window)
        self.actionFatores_vari_veis.triggered.connect(self.open_config_window)
        self.actionSobre.triggered.connect(self.open_info_window)
        self.actionConsultar_laudo_2.triggered.connect(self.open_get_report_window)
        self.actionLogo.triggered.connect(self.open_upload_logo_window)
        self.actionBackup.triggered.connect(self.open_backup_window)
        self.actionSelo.triggered.connect(self.open_upload_report_stamp_window)

        

        

    def closeEvent(self, event):
        for window in self.open_windows[:]:  # Iterar em uma cópia para evitar conflitos
            window.close()
        self.open_windows.clear()
        event.accept()

    def open_requester_window(self) -> None:
        dialog = RequesterWindow()
        self.add_window(dialog)

    def open_config_window(self) -> None:
        dialog = ConfigurationWindow()
        self.add_window(dialog)

    def open_info_window(self) -> None:
        dialog = InfoWindow()
        self.add_window(dialog)

    def open_get_report_window(self) -> None:
        dialog = GetReport()
        self.add_window(dialog)

    def open_upload_logo_window(self) -> None:
        dialog = UploadLogo()
        self.add_window(dialog)

    def open_upload_report_stamp_window(self) -> None:
        dialog = UploadReportStamp()
        self.add_window(dialog)

    def open_backup_window(self) -> None:
        dialog = BackupWindow()
        self.add_window(dialog)

    def add_window(self, dialog):
        self.open_windows.append(dialog)
        dialog.setAttribute(Qt.WA_DeleteOnClose)  # Remove referência ao fechar
        dialog.destroyed.connect(lambda: self.open_windows.remove(dialog))  # Remove da lista quando deletado
        dialog.show()  # Exibe a janela de forma não modal



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
