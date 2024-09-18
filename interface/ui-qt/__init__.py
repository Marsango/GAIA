import sqlite3
import sys
from backend.classes.utils import handle_exception
from PySide6.QtSvgWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QMainWindow, QDialog, QCompleter, QWidget, QTableWidgetItem, QAbstractItemView)
from datetime import datetime
from backend.classes.Address import Address
from backend.classes.Person import Person
from backend.classes.Database import Database
from backend.classes.Company import Company
from main_window import Ui_MainWindow
from register_person import RegisterPersonDialog
from register_company import RegisterCompanyDialog
from requester_window import RequesterDialog
from error_window import ErrorDialog
from sucessful_register import SucessfulDialog

class SucessfulRegister(QDialog, SucessfulDialog):
    def __init__(self, **kwargs) -> None:
        super(SucessfulRegister, self).__init__()
        self.setupUi(self)
        message: str = kwargs.get('sucess_message')
        if message:
            self.label.setText(message)
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
        self.current_person_id = None
        self.setupUi(self)
        self.setWindowTitle('Registro de Pessoa Física')
        self.register_button.clicked.connect(self.register_action)
        self.create_country_completer()
        self.country_input.editingFinished.connect(self.country_changed)
        self.state_input.editingFinished.connect(self.state_changed)
        self.city_input.editingFinished.connect(self.city_changed)
        self.mode = 'register'

    def edit_mode(self, person_data) -> None:
        self.country_input.insert(person_data['country'])
        self.state_input.insert(person_data['state'])
        self.city_input.insert(person_data['city'])
        self.street_input.insert(person_data['street'])
        self.address_number_input.insert(str(person_data['address_number']))
        self.cep_input.insert(person_data['cep'])
        self.name_input.insert(person_data['name'])
        self.email_input.insert(person_data['email'])
        self.cpf_input.insert(person_data['cpf'])
        self.birth_date_input.insert(person_data['birth_date'])
        print(person_data['birth_date'])
        print(type(person_data['birth_date']))
        self.phone_number_input.insert(person_data['phone_number'])
        self.register_button.setText("Salvar alterações")
        self.setWindowTitle('Edição de registro de Pessoa Física')
        self.mode = 'edit'
        self.current_person_id = int(person_data['id'])


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

        address: Address = Address(country=self.country_input.text(), state=self.state_input.text(),
                                   city=self.city_input.text(), street=self.street_input.text(),
                                   address_number=self.address_number_input.text(), cep=self.cep_input.text())
        person: Person = Person(name=self.name_input.text(), email=self.email_input.text(),
                                cpf=self.cpf_input.text().replace('.', '').replace('-', ''),
                                birth_date=self.birth_date_input.text(),
                                phone_number=self.phone_number_input.text()
                                .replace('-', '').replace('(', '').replace(')', ''), address=address)
        if self.mode == 'register':
            db.insert_person(person, address)
            sucess_text: str = "Solicitante registrado com sucesso!"
        elif self.mode == 'edit':
            db.edit_person(person, address, self.current_person_id)
            sucess_text: str = "Alterações salvas com sucesso!"
        widget: SucessfulRegister = SucessfulRegister(sucess_message=sucess_text)
        widget.exec()
    # except Exception as e:
    #     error = handle_exception(e)
    #     print(e)
    #     print(e.__traceback__)
    #     widget: ErrorWindow = ErrorWindow(error)
    #     widget.exec()

        db.close_connection()




class RegisterCompany(QDialog, RegisterCompanyDialog):
    def __init__(self) -> None:
        super(RegisterCompany, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Registro de Pessoa Jurídica')
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


class RequesterWindow(QDialog, RequesterDialog):
    def __init__(self) -> None:
        super(RequesterWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Solicitantes registrados')
        self.current_table = 'person'
        self.add.clicked.connect(self.register_person)
        self.edit.clicked.connect(self.edit_person)
        self.requester_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.requester_type.currentTextChanged.connect(self.type_change)
        self.refresh_table()

    def type_change(self):
        if self.requester_type.currentText() == 'Pessoa física':
            self.create_person_table()
            self.add.clicked.disconnect(self.register_company)
            self.add.clicked.connect(self.register_person)
            self.edit.clicked.connect(self.edit_person)
        elif self.requester_type.currentText() == 'Pessoa jurídica':
            self.create_company_table()
            self.add.clicked.disconnect(self.register_person)
            self.add.clicked.connect(self.register_company)


    def edit_person(self):
        dialog: RegisterPerson = RegisterPerson()
        selected_items: list[QTableWidgetItem] = self.requester_table.selectedIndexes()
        if len(selected_items) == 0:
            widget: ErrorWindow = ErrorWindow("Você deve selecionar um solicitante para editar.")
            widget.exec()
            return
        for data in selected_items:
            if data.row() != selected_items[0].row():
                widget: ErrorWindow = ErrorWindow("Você só pode editar um solicitante por vez.")
                widget.exec()
                return
        row: int = selected_items[0].row()
        id: str = self.requester_table.item(row, 0).text()
        db: Database = Database()
        person: sqlite3.Row = db.get_persons(id=id)[0]
        dialog.edit_mode(person)
        dialog.exec()
        self.refresh_table()

    def create_person_table(self):
        if self.current_table == 'company':
            self.requester_table.setRowCount(0)
            self.requester_table.setColumnCount(7)
            self.requester_table.setHorizontalHeaderItem(2, QTableWidgetItem("Nascimento"))
            self.requester_table.setHorizontalHeaderItem(3, QTableWidgetItem("CPF"))
            self.requester_table.setHorizontalHeaderItem(4, QTableWidgetItem("Telefone"))
            self.requester_table.setHorizontalHeaderItem(5, QTableWidgetItem("E-mail"))
            self.requester_table.setHorizontalHeaderItem(6, QTableWidgetItem("Endereço"))
            self.current_table = 'person'
            self.refresh_table()

    def create_company_table(self):
        if self.current_table == 'person':
            self.requester_table.setRowCount(0)
            self.requester_table.setColumnCount(6)
            self.requester_table.setHorizontalHeaderItem(2, QTableWidgetItem("CNPJ"))
            self.requester_table.setHorizontalHeaderItem(3, QTableWidgetItem("Telefone"))
            self.requester_table.setHorizontalHeaderItem(4, QTableWidgetItem("E-mail"))
            self.requester_table.setHorizontalHeaderItem(5, QTableWidgetItem("Endereço"))
            self.current_table = 'company'
            self.refresh_table()

    def refresh_table(self):
        db: Database = Database()
        if self.current_table == 'person':
            persons: list[sqlite3.Row] = db.get_persons()
            self.requester_table.setRowCount(0)
            for person in persons:
                row_position: int = self.requester_table.rowCount()
                self.requester_table.insertRow(row_position)
                self.requester_table.setItem(row_position, 0, QTableWidgetItem(str(person['id'])))
                self.requester_table.setItem(row_position, 1, QTableWidgetItem(person['name']))
                self.requester_table.setItem(row_position, 2, QTableWidgetItem(person['birth_date']))
                self.requester_table.setItem(row_position, 3, QTableWidgetItem(person['cpf']))
                self.requester_table.setItem(row_position, 4, QTableWidgetItem(person['phone_number']))
                self.requester_table.setItem(row_position, 5, QTableWidgetItem(person['email']))
                self.requester_table.setItem(row_position, 6, QTableWidgetItem(f"{person['street']}, {person['address_number']} - {person['cep']}, {person['city']}, {person['state']}, {person['country']}"))
        elif self.current_table == 'company':
            companies: list[sqlite3.Row] = db.get_companies()
            self.requester_table.setRowCount(0)
            for company in companies:
                row_position = self.requester_table.rowCount()
                self.requester_table.insertRow(row_position)
                self.requester_table.setItem(row_position, 0, QTableWidgetItem(str(company['id'])))
                self.requester_table.setItem(row_position, 1, QTableWidgetItem(company['company_name']))
                self.requester_table.setItem(row_position, 2, QTableWidgetItem(company['cnpj']))
                self.requester_table.setItem(row_position, 3, QTableWidgetItem(company['phone_number']))
                self.requester_table.setItem(row_position, 4, QTableWidgetItem(company['email']))
                self.requester_table.setItem(row_position, 5, QTableWidgetItem(f"{company['street']}, {company['address_number']} - {company['address']}, {company['city']}, {company['state']}, {company['country']}"))

    def register_person(self):
        dialog: RegisterPerson = RegisterPerson()
        dialog.exec()
        self.refresh_table()

    def register_company(self):
        dialog: RegisterCompany = RegisterCompany()
        dialog.exec()
        self.refresh_table()

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('GAIA SOFTWARE')
        self.showMaximized()
        self.svg_widget = QSvgWidget('images/background.svg')
        self.horizontalLayout.addWidget(self.svg_widget)
        self.actionSolicitantes.triggered.connect(self.open_requesters_window)

    def open_requesters_window(self) -> None:
        dialog: RequesterWindow = RequesterWindow()
        dialog.exec()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
