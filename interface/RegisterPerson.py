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
from datetime import datetime

class RegisterPerson(QDialog, RegisterPersonDialog):
    # Cidades próximas a Pato Branco por estado
    CIDADES_PROXIMAS = {
        "Paraná": [
            "Pato Branco", "Marmeleiro", "Coronel Vivida", "Sulina", "Enéas Marques",
            "Renascença", "Pranchita", "Crespo", "Santo Antônio do Sudoeste", 
            "Capanema", "Ampére", "Neves", "Clevelândia", "Realeza", "Francisco Beltrão"
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

    def __init__(self) -> None:
        super(RegisterPerson, self).__init__()
        self.requester_id: int | None = None
        self.current_person_id: int | None = None
        self.setupUi(self)
        self.cep_input.setMaxLength(8)
        self.setWindowTitle('Registro de Pessoa Física')
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
        self.mode: str = 'register'
    
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
            print(f" Erro ao configurar autocomplete: {e}")

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
        # Converter data de YYYY-MM-DD para DD/MM/YYYY
        birth_date = person_data['birth_date']
        if birth_date:
            birth_date_formatted = self._convert_date_to_display(birth_date)
            self.birth_date_input.setText(birth_date_formatted)
        self.phone_number_input.setText(person_data['phone_number'])
        self.register_button.setText("Salvar alterações")
        self.setWindowTitle('Edição de registro de Pessoa Física')
        self.mode = 'edit'
        self.current_person_id = int(person_data['id'])
        self.requester_id = int(person_data['requester_id'])

    def _convert_date_to_display(self, date_str: str) -> str:
        """Converte data de YYYY-MM-DD para DD/MM/YYYY"""
        if not date_str:
            return ""
        
        try:
            date_str = date_str.strip()
            
            # Se já está em DD/MM/YYYY, retorna como está
            if len(date_str) == 10 and date_str[2] == '/' and date_str[5] == '/':
                return date_str
            
            # Converter de YYYY-MM-DD para DD/MM/YYYY
            if len(date_str) == 10 and date_str[4] == '-' and date_str[7] == '-':
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                converted = date_obj.strftime("%d/%m/%Y")
                print(f"✓ Data exibida: {date_str} → {converted}")
                return converted
            
            print(f" Formato de data não reconhecido na exibição: {date_str}")
            return date_str
        except Exception as e:
            print(f" Erro ao converter data para exibição: {e}")
            return date_str

    def _convert_date_to_iso(self, date_str: str) -> str:
        """Converte data de DD/MM/YYYY para YYYY-MM-DD"""
        if not date_str:
            return ""
        
        try:
            date_str = date_str.strip()
            
            # Se já está em YYYY-MM-DD, retorna como está
            if len(date_str) == 10 and date_str[4] == '-' and date_str[7] == '-':
                return date_str
            
            # Converter de DD/MM/YYYY para YYYY-MM-DD
            if len(date_str) == 10 and date_str[2] == '/' and date_str[5] == '/':
                date_obj = datetime.strptime(date_str, "%d/%m/%Y")
                converted = date_obj.strftime("%Y-%m-%d")
                print(f"✓ Data convertida: {date_str} → {converted}")
                return converted
            
            # Formato não reconhecido
            print(f" Formato de data não reconhecido: {date_str}")
            return ""
        except Exception as e:
            print(f" Erro ao converter data {date_str}: {e}")
            return ""

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
        state = self.state_input.text()
        
        # Usar lista de cidades próximas se existir
        if state in self.CIDADES_PROXIMAS:
            cities = self.CIDADES_PROXIMAS[state]
        else:
            # Fallback: tentar carregarde banco de dados
            db = Database()
            cities = db.get_cities(state)
            db.close_connection()
        
        completer = QCompleter(cities, self)
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

            # Validação de email
            email = self.email_input.text().strip()
            if not email:
                raise ValueError("O campo 'Email' deve ser preenchido!")
            if '@' not in email or '.' not in email:
                raise ValueError("Email inválido! Use o formato: exemplo@dominio.com")

            # Validação de nome
            name = self.name_input.text().strip()
            if not name:
                raise ValueError("O campo 'Nome' deve ser preenchido!")

            # Validação de CPF
            cpf = self.cpf_input.text().replace('.', '').replace('-', '').strip()
            if not cpf or len(cpf) != 11:
                raise ValueError("CPF inválido! Deve ter 11 dígitos")
            
            # Validação de data de nascimento
            birth_date_raw = self.birth_date_input.text().strip()
            if not birth_date_raw:
                raise ValueError("O campo 'Data de Nascimento' deve ser preenchido!")
            
            # NÃO converter aqui! A classe Person espera DD/MM/YYYY
            # Apenas validar o formato
            if len(birth_date_raw) != 10 or birth_date_raw[2] != '/' or birth_date_raw[5] != '/':
                raise ValueError("Data de nascimento inválida! Use o formato DD/MM/YYYY")
            
            # Tentar fazer parse para validar a data
            try:
                from datetime import datetime
                birth_date_obj = datetime.strptime(birth_date_raw, "%d/%m/%Y").date()
            except ValueError:
                raise ValueError("Data de nascimento inválida! Verifique se a data existe")

            # Impedir datas futuras
            today = datetime.today().date()
            if birth_date_obj > today:
                raise ValueError("Data de nascimento não pode ser futura")

            # Validar faixa etária (18 a 120 anos)
            age = today.year - birth_date_obj.year - ((today.month, today.day) < (birth_date_obj.month, birth_date_obj.day))
            if age < 18:
                raise ValueError(f"Idade mínima é 18 anos. Idade atual: {age} anos")
            if age > 120:
                raise ValueError(f"Data de nascimento muito antiga. Idade calculada: {age} anos")

            address: Address = Address(country=self.country_input.text(), state=self.state_input.text(),
                                       city=self.city_input.text(), street=street,
                                       address_number=address_number, cep=cep)
            person: Person = Person(name=name, email=email,
                                    cpf=cpf,
                                    birth_date=birth_date_raw,
                                    phone_number=self.phone_number_input.text()
                                    .replace('-', '').replace('(', '').replace(')', ''), address=address)
            if self.mode == 'register':
                db.insert_person(person, address)
                success_text: str = "Solicitante registrado com sucesso!"
            elif self.mode == 'edit':
                
                try:
                    result = db.edit_person(person, address, self.current_person_id, self.requester_id)
                    
                    if result:
                        success_text: str = "Alterações salvas com sucesso!"
                    else:
                        raise ValueError("Falha ao salvar alterações - verifique o console para detalhes")
                except Exception as edit_error:
                    print(f"\n ERRO CAPTURADO no RegisterPerson:")
                    print(f"   Tipo: {type(edit_error).__name__}")
                    print(f"   Mensagem: {str(edit_error)}")
                    import traceback
                    traceback.print_exc()
                    raise  # Re-throw para ser pego pelo handler externo
                    
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