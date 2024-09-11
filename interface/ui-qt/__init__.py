import sys
from backend.classes.utils import handle_exception
from PySide6.QtSvgWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QMainWindow, QDialog, QCompleter)
from datetime import datetime
from backend.classes.Address import Address
from backend.classes.Person import Person
from backend.classes.Database import Database
from backend.classes.Company import Company
from main_window import Ui_MainWindow
from register_person import RegisterPersonDialog
from register_company import RegisterCompanyDialog
from error_window import ErrorDialog
from sucessful_register import SucessfulDialog

class SucessfulRegister(QDialog, SucessfulDialog):
    def __init__(self) -> None:
        super(SucessfulRegister, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.close)

class ErrorWindow(QDialog, ErrorDialog):
    def __init__(self, error) -> None:
        super(ErrorWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Erro!')
        self.label_2.setText(error)
        self.pushButton.clicked.connect(self.close)


class RegisterPerson(QDialog, RegisterPersonDialog):
    def __init__(self) -> None:
        super(RegisterPerson, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Registro de Pessoa Física')
        self.register_button.clicked.connect(self.register_action)
        self.create_country_completer()
        self.country_input.editingFinished.connect(self.country_changed)
        self.state_input.editingFinished.connect(self.state_changed)
        self.city_input.editingFinished.connect(self.city_changed)


    def create_country_completer(self) -> None:
        db: Database = Database()
        completer: QCompleter = QCompleter(db.get_countries(), self)
        db.close_connection()
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.country_input.setCompleter(completer)

    def country_changed(self) -> None:
        db: Database = Database()
        completer: QCompleter = QCompleter(db.get_states(self.country_input.text()), self)
        db.close_connection()
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.state_input.setCompleter(completer)

    def state_changed(self) -> None:
        db: Database = Database()
        completer: QCompleter = QCompleter(db.get_cities(self.state_input.text()), self)
        db.close_connection()
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.city_input.setCompleter(completer)

    def city_changed(self) -> None:
        db: Database = Database()
        completer: QCompleter = QCompleter(db.get_streets(self.city_input.text()), self)
        db.close_connection()
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.street_input.setCompleter(completer)


    def register_action(self) -> None:
        db: Database = Database()
        try:
            address: Address = Address(country=self.country_input.text(), state=self.state_input.text(),
                                       city=self.city_input.text(), street=self.street_input.text(),
                                       address_number=self.address_number_input.text(), cep=self.cep_input.text())
            person: Person = Person(name=self.name_input.text(), email=self.email_input.text(),
                                    cpf=self.cpf_input.text().replace('.', '').replace('-', ''),
                                    birth_date=self.birth_date_input.text(),
                                    phone_number=self.phone_number_input.text()
                                    .replace('-', '').replace('(', '').replace(')', ''), address=address)
            db.insert_person(person, address)
            widget: SucessfulRegister = SucessfulRegister()
            widget.exec()
        except Exception as e:
            error = handle_exception(e)
            widget: ErrorWindow = ErrorWindow(error)
            widget.exec()

        db.close_connection()


class RegisterCompany(QDialog, RegisterCompanyDialog):
    def __init__(self) -> None:
        super(RegisterCompany, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Registro de Pessoa Jurídica')
        self.register_button.clicked.connect(self.register_action)

    def register_action(self) -> None:
        db: Database = Database()
        try:
            address: Address = Address(country=self.country_input.text(), state=self.state_input.text(),
                                       city=self.city_input.text(), street=self.street_input.text(),
                                       address_number=self.address_number_input.text(), cep=self.cep_input.text())
            company: Company = Company(company_name=self.company_name_input.text(), email=self.email_input.text(),
                                       cnpj=self.cnpj_input.text().replace('.', '').replace('/', '').replace('-', ''),
                                       phone_number=self.phone_number_input.text()
                                       .replace('(', '').replace(')', '').replace('-', ''), address=address)
            db.insert_company(company, address)
            widget: SucessfulRegister = SucessfulRegister()
            widget.exec()
        except Exception as e:
            error = handle_exception(e)
            widget: ErrorWindow = ErrorWindow(error)
            widget.exec()

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
        self.actionPessoa_Jur_dica.triggered.connect(self.register_company_window)

    def register_person_window(self) -> None:
        widget: RegisterPerson = RegisterPerson()
        widget.exec()

    def register_company_window(self) -> None:
        widget: RegisterCompany = RegisterCompany()
        widget.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
