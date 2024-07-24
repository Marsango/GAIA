from PySide6.QtWidgets import (QApplication, QMainWindow, QDialog)
from PySide6.QtCore import (QSize, Qt, SIGNAL)
from PySide6 import QtCore
from main_window import Ui_MainWindow
from register_person import Ui_Form
import sys, os
from PySide6.QtSvgWidgets import *
from backend.classes.Person import Person
from backend.classes.Address import Address


class Register_Person(QDialog, Ui_Form):
    def __init__(self) -> None:
        super(Register_Person, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Registro de Pessoa Física')
        self.register_button.clicked.connect(self.register_action)

    def register_action(self) -> None:
        address: Address = Address(country=self.country_input.text(), state=self.state_input.text(),
                                   city=self.city_input.text(), street=self.street_input.text(),
                                   number=self.address_number_input.text(), cep=self.cep_input.text())
        person: Person = Person(name=self.name_input.text(), email=self.email_input.text(),
                                cpf=self.cpf_input.text(), birth_date=self.birth_date_input(),
                                phone_number=self.phone_number_input(), address=address)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('GAIA SOFTWARE')
        self.showMaximized()
        self.svg_widget = QSvgWidget('images/background.svg')
        self.horizontalLayout.addWidget(self.svg_widget)
        self.actionPessoa_F_sica.triggered.connect(self.register_person_window)

    def register_person_window(self) -> None:
        widget: Register_Person = Register_Person()
        widget.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
