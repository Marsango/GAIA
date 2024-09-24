import sys
from PySide6.QtSvgWidgets import *
from PySide6.QtWidgets import (QApplication, QMainWindow)
from base_windows.main_window import Ui_MainWindow
from RequesterWindow import RequesterWindow
from PropertyWindow import PropertyWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('GAIA SOFTWARE')
        self.showMaximized()
        self.svg_widget = QSvgWidget('images/background.svg')
        self.horizontalLayout.addWidget(self.svg_widget)
        self.actionSolicitantes.triggered.connect(self.open_requester_window)


    def open_requester_window(self) -> None:
        dialog: RequesterWindow = RequesterWindow()
        dialog.exec()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
