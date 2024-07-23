from PySide6.QtWidgets import(QApplication, QMainWindow)
from PySide6.QtCore import (QSize, Qt)
from PySide6 import QtCore
from main_window import Ui_MainWindow
import sys, os
from PySide6.QtSvgWidgets import *

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('GAIA SOFTWARE')
        self.showMaximized()
        self.svg_widget = QSvgWidget('images/background.svg')
        self.horizontalLayout.addWidget(self.svg_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()