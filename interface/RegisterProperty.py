import os

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (QDialog, QCompleter)
from interface.base_windows.register_property import RegisterPropertyDialog
from PySide6.QtCore import Qt
from backend.classes.Property import Property
from backend.classes.Address import Address
from interface.AlertWindow import AlertWindow
from backend.classes.Database import Database
from backend.classes.utils import handle_exception


class RegisterProperty(QDialog, RegisterPropertyDialog):
    # Cidades próximas a Pato Branco por estado
    CIDADES_PROXIMAS = {
        "Paraná": [
            "Pato Branco", "Marmeleiro", "Coronel Vivida", "Sulina", "Enéas Marques",
            "Renascença", "Pranchita", "Crespo", "Santo Antônio do Sudoeste", 
            "Capanema", "Ampére", "Neves", "Clevelândia", "Realeza"
        ],
        "Santa Catarina": [
            "Chapecó", "Xanxerê", "Caxambu do Sul", "Tapejara", "Santa Cecília",
            "Lebon Régis", "Bom Jesus do Oeste", "Anita Garibaldi", "Vargem",
            "Iomerê", "Tigrinhos", "Cambará do Sul", "Maravilha"
        ],
        "Rio Grande do Sul": [
            "Alegrete", "Rosário do Sul", "Maçambá", "Lavras do Sul", "Uruguaiana",
            "São Gabriel", "Bagé", "Santana do Livramento", "Dom Pedrito",
            "Caçapava do Sul", "Pinheiro Machado", "Encruzilhada do Sul"
        ]
    }

    def __init__(self, requester_id: int) -> None:
        super(RegisterProperty, self).__init__()
        self.current_property_id: int | None = None
        self.setupUi(self)
        self.setWindowTitle('Registro de propriedade')
        self.setWindowIcon(QPixmap(os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "interface",
            "images"
        ).replace("\\", "/") + "/GAIA_icon.png"))
        self.register_button.clicked.connect(self.register_action)
        # Conectar eventos de mudança
        self.state_input.editingFinished.connect(self.state_changed)
        # Autocomplete otimizado - consulta apenas 1 vez ao abrir
        self.setup_autocomplete()
        self.requester_id: int = requester_id
        self.mode: str = 'register'

    def edit_mode(self, property_data) -> None:
        self.country_input.setText(property_data['country'])
        self.state_input.setText(property_data['state'])
        self.city_input.setText(property_data['city'])
        self.name_input.setText(property_data['name'])
        self.registration_number_input.setText(str(property_data['registration_number']))
        self.location_input.setText(property_data['location'])

        self.register_button.setText("Salvar alterações")
        self.setWindowTitle('Edição de registro de propriedade')
        self.mode = 'edit'
        self.current_property_id = int(property_data['id'])

    def setup_autocomplete(self) -> None:
        """Configura autocomplete com dados estáticos - sem múltiplas conexões"""
        try:
            # Lista estática de países
            countries = ["Brasil"]
            completer = QCompleter(countries, self)
            completer.setCaseSensitivity(Qt.CaseInsensitive)
            self.country_input.setCompleter(completer)
            
            # Apenas estados próximos a Pato Branco
            states = ["Paraná", "Santa Catarina", "Rio Grande do Sul"]
            state_completer = QCompleter(states, self)
            state_completer.setCaseSensitivity(Qt.CaseInsensitive)
            self.state_input.setCompleter(state_completer)
        except Exception as e:
            print(f"⚠️ Erro ao configurar autocomplete: {e}")


    def state_changed(self) -> None:
        state = self.state_input.text()
        
        # Usar lista de cidades próximas se existir
        if state in self.CIDADES_PROXIMAS:
            cities = self.CIDADES_PROXIMAS[state]
        else:
            # Fallback: tentar carregar do banco de dados
            db = Database()
            cities = db.get_cities(state)
            db.close_connection()
        
        completer = QCompleter(cities, self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.city_input.setCompleter(completer)

    def register_action(self) -> None:
        db = Database()
        try:
            # Criar endereço apenas com país, estado e cidade
            # Propriedade não usa CEP, rua ou número
            address: Address = Address(
                country=self.country_input.text(),
                state=self.state_input.text(),
                city=self.city_input.text(),
                street='',
                address_number='',
                cep=''
            )
            property: Property = Property(
                name=self.name_input.text(),
                registration_number=self.registration_number_input.text(),
                localizacao=self.location_input.text()
            )
            if self.mode == 'register':
                db.insert_property(property, self.requester_id, address)
                success: str = "Propriedade registrada com sucesso!"
            else:
                db.edit_property(property, self.current_property_id, address)
                success: str = "Alterações salvas com sucesso!"
            widget: AlertWindow = AlertWindow(success)
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
        self.name_input.clear()
        self.registration_number_input.clear()
        self.location_input.clear()