import sys

from PySide6.QtSvgWidgets import *
from PySide6.QtWidgets import (QApplication, QMainWindow, QDialog)
from datetime import datetime
from backend.classes.Address import Address
from backend.classes.Person import Person
from backend.classes.Database import Database
from main_window import Ui_MainWindow
from register_person import Ui_Form


class RegisterPerson(QDialog, Ui_Form):
    def __init__(self) -> None:
        super(RegisterPerson, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Registro de Pessoa Física')
        self.register_button.clicked.connect(self.register_action)

    def register_action(self) -> None:
        db = Database()
        address: Address = Address(country=self.country_input.text(), state=self.state_input.text(),
                                   city=self.city_input.text(), street=self.street_input.text(),
                                   address_number=int(self.address_number_input.text()), cep=self.cep_input.text())
        person: Person = Person(name=self.name_input.text(), email=self.email_input.text(),
                                cpf=self.cpf_input.text(),
                                birth_date=datetime.strptime(self.birth_date_input.text(), '%d/%m/%Y'),
                                phone_number=self.phone_number_input.text(), address=address)
        db.insert_person(person, address)
        db.close_connection()

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
        widget: RegisterPerson = RegisterPerson()
        widget.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
