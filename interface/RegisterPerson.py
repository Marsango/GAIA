import os

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (QDialog, QCompleter)
from interface.base_windows.register_person import RegisterPersonDialog
from PySide6.QtCore import Qt
from backend.classes.Address import Address
from backend.classes.Person import Person
from interface.AlertWindow import AlertWindow
from backend.classes.Database import Database
from backend.classes.utils import handle_exception

class RegisterPerson(QDialog, RegisterPersonDialog):
    def __init__(self) -> None:
        super(RegisterPerson, self).__init__()
        self.requester_id: int | None = None
        self.current_person_id: int | None = None
        self.setupUi(self)
        self.setWindowTitle('Registro de Pessoa Física')
        self.setWindowIcon(QPixmap(os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "interface",
            "images"
        ).replace("\\", "/") + "/GAIA_icon.png"))
        self.register_button.clicked.connect(self.register_action)
        # Autocomplete otimizado - consulta apenas 1 vez ao abrir
        self.setup_autocomplete()
        self.mode: str = 'register'
    
    def setup_autocomplete(self) -> None:
        """Configura autocomplete com dados estáticos - sem múltiplas conexões"""
        try:
            # Lista estática de países
            countries = ["Brasil"]
            completer = QCompleter(countries, self)
            completer.setCaseSensitivity(Qt.CaseInsensitive)
            self.country_input.setCompleter(completer)
            
            # Listas estáticas de estados brasileiros
            states = ["Acre", "Alagoas", "Amapá", "Amazonas", "Bahia", "Ceará", 
                     "Distrito Federal", "Espírito Santo", "Goiás", "Maranhão", 
                     "Mato Grosso", "Mato Grosso do Sul", "Minas Gerais", "Pará", 
                     "Paraíba", "Paraná", "Pernambuco", "Piauí", "Rio de Janeiro", 
                     "Rio Grande do Norte", "Rio Grande do Sul", "Rondônia", "Roraima", 
                     "Santa Catarina", "São Paulo", "Sergipe", "Tocantins"]
            state_completer = QCompleter(states, self)
            state_completer.setCaseSensitivity(Qt.CaseInsensitive)
            self.state_input.setCompleter(state_completer)
        except Exception as e:
            print(f"⚠️ Erro ao configurar autocomplete: {e}")

    def edit_mode(self, person_data) -> None:
        self.country_input.setText(person_data['country'])
        self.state_input.setText(person_data['state'])
        self.city_input.setText(person_data['city'])
        self.street_input.setText(person_data['street'])
        self.address_number_input.setText(str(person_data['address_number']))
        self.cep_input.setText(person_data['cep'])
        self.name_input.setText(person_data['name'])
        self.email_input.setText(person_data['email'])
        self.cpf_input.setText(person_data['cpf'])
        self.birth_date_input.setText(person_data['birth_date'])
        self.phone_number_input.setText(person_data['phone_number'])
        self.register_button.setText("Salvar alterações")
        self.setWindowTitle('Edição de registro de Pessoa Física')
        self.mode = 'edit'
        self.current_person_id = int(person_data['id'])
        self.requester_id = int(person_data['requester_id'])


    def create_country_completer(self) -> None:
        db = Database()
        completer: QCompleter = QCompleter(db.get_countries(), self)
        db.close_connection()
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.country_input.setCompleter(completer)

    def country_changed(self) -> None:
        db = Database()
        completer: QCompleter = QCompleter(db.get_states(self.country_input.text()), self)
        db.close_connection()
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.state_input.setCompleter(completer)

    def state_changed(self) -> None:
        db = Database()
        completer: QCompleter = QCompleter(db.get_cities(self.state_input.text()), self)
        db.close_connection()
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.city_input.setCompleter(completer)

    def city_changed(self) -> None:
        db = Database()
        completer: QCompleter = QCompleter(db.get_streets(self.city_input.text()), self)
        db.close_connection()
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.street_input.setCompleter(completer)


    def register_action(self) -> None:
        db = Database()
        try:
            # Validação de campos obrigatórios do endereço
            cep = self.cep_input.text().replace('-', '').strip()
            street = self.street_input.text().strip()
            address_number = self.address_number_input.text().strip()
            
            if not cep:
                raise ValueError("O campo 'CEP' deve ser preenchido!")
            if not street:
                raise ValueError("O campo 'Rua' deve ser preenchido!")
            if not address_number:
                raise ValueError("O campo 'Número' deve ser preenchido!")

            address: Address = Address(country=self.country_input.text(), state=self.state_input.text(),
                                       city=self.city_input.text(), street=street,
                                       address_number=address_number, cep=cep)
            person: Person = Person(name=self.name_input.text(), email=self.email_input.text(),
                                    cpf=self.cpf_input.text().replace('.', '').replace('-', ''),
                                    birth_date=self.birth_date_input.text(),
                                    phone_number=self.phone_number_input.text()
                                    .replace('-', '').replace('(', '').replace(')', ''), address=address)
            if self.mode == 'register':
                db.insert_person(person, address)
                success_text: str = "Solicitante registrado com sucesso!"
            elif self.mode == 'edit':
                db.edit_person(person, address, self.current_person_id, self.requester_id)
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

    def clean_input(self):
        self.country_input.clear()
        self.state_input.clear()
        self.city_input.clear()
        self.street_input.clear()
        self.address_number_input.clear()
        self.cep_input.clear()
        self.name_input.clear()
        self.birth_date_input.clear()
        self.email_input.clear()
        self.cpf_input.clear()
        self.phone_number_input.clear()