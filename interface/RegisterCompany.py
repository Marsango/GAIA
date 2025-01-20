import os

from PySide6.QtGui import QPixmap

from interface.base_windows.register_company import RegisterCompanyDialog
from backend.classes.Company import Company
from backend.classes.Address import Address
from PySide6.QtCore import Qt
from interface.AlertWindow import AlertWindow
from PySide6.QtWidgets import (QDialog, QCompleter)
from backend.classes.Database import Database
from backend.classes.utils import handle_exception


class RegisterCompany(QDialog, RegisterCompanyDialog):
    def __init__(self) -> None:
        super(RegisterCompany, self).__init__()
        self.requester_id: int | None = None
        self.current_company_id: int | None = None
        self.setupUi(self)
        self.setWindowTitle('Registro de Pessoa Jurídica')
        self.setWindowIcon(QPixmap(os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "interface",
            "images"
        ).replace("\\", "/") + "/logo_lab.png"))
        self.register_button.clicked.connect(self.register_action)
        self.create_country_completer()
        self.country_input.editingFinished.connect(self.country_changed)
        self.state_input.editingFinished.connect(self.state_changed)
        self.city_input.editingFinished.connect(self.city_changed)
        self.mode = 'register'

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
                                       address_number=self.address_number_input.text(), cep=self.cep_input.text().replace('-', ''))
            company: Company = Company(company_name=self.company_name_input.text(), email=self.email_input.text(),
                                       cnpj=self.cnpj_input.text().replace('.', '').replace('/', '').replace('-', ''),
                                       phone_number=self.phone_number_input.text()
                                       .replace('(', '').replace(')', '').replace('-', ''), address=address)
            if self.mode == 'register':
                db.insert_company(company, address)
                success_text: str = "Solicitante registrado com sucesso!"
            else:
                db.edit_company(company, address, self.current_company_id, self.requester_id)
                success_text: str = "Alterações salvas com sucesso!"
            widget: AlertWindow = AlertWindow(success_text)
            widget.exec()
            if self.mode == 'register':
                self.clean_input()
        except Exception as e:
            error = handle_exception(e)
            widget: AlertWindow = AlertWindow(error)
            widget.exec()

        db.close_connection()

    def edit_mode(self, company_data) -> None:
        self.country_input.clear()
        self.state_input.clear()
        self.city_input.clear()
        self.street_input.clear()
        self.address_number_input.clear()
        self.cep_input.clear()
        self.company_name_input.clear()
        self.email_input.clear()
        self.cnpj_input.clear()
        self.phone_number_input.clear()

        self.country_input.setText(company_data['country'])
        self.state_input.setText(company_data['state'])
        self.city_input.setText(company_data['city'])
        self.street_input.setText(company_data['street'])
        self.address_number_input.setText(str(company_data['address_number']))
        self.cep_input.setText(company_data['cep'])
        self.company_name_input.setText(company_data['company_name'])
        self.email_input.setText(company_data['email'])
        self.cnpj_input.setText(company_data['cnpj'])
        self.phone_number_input.setText(company_data['phone_number'])

        self.register_button.setText("Salvar alterações")
        self.setWindowTitle('Edição de registro de Pessoa Física')
        self.mode = 'edit'
        self.current_company_id = int(company_data['id'])
        self.requester_id = int(company_data['requester_id'])

    def clean_input(self):
        self.country_input.clear()
        self.state_input.clear()
        self.city_input.clear()
        self.street_input.clear()
        self.address_number_input.clear()
        self.cep_input.clear()
        self.company_name_input.clear()
        self.email_input.clear()
        self.cnpj_input.clear()
        self.phone_number_input.clear()