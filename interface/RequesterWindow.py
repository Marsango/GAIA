import os
import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QDialog, QTableWidgetItem, QAbstractItemView, QHeaderView)
from interface.base_windows.requester_window import RequesterDialog
from interface.DeleteConfirmation import DeleteConfirmation
from interface.AlertWindow import AlertWindow
from backend.classes.utils import handle_exception
from interface.RegisterCompany import RegisterCompany
from interface.RegisterPerson import RegisterPerson
from interface.PropertyWindow import PropertyWindow
from backend.classes.Database import Database
import sqlite3


def get_image_path(filename: str) -> str:
    """Resolve imagens tanto no código-fonte quanto no executável PyInstaller."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, "images", filename)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", filename)


class RequesterWindow(QDialog, RequesterDialog):
    def __init__(self) -> None:
        super(RequesterWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Solicitantes registrados')

        icon_path = get_image_path("GAIA_icon.ico")
        if not os.path.exists(icon_path):
            icon_path = get_image_path("GAIA_icon.png")
        self.setWindowIcon(QIcon(icon_path))

        self.requester_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.requester_table.verticalHeader().setVisible(False)
        self.add.clicked.connect(self.register_person)
        self.edit.clicked.connect(self.edit_requester)
        self.delete_2.clicked.connect(self.delete_requester)
        self.current_table_type = 'person'
        self.requester_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.requester_type.currentTextChanged.connect(self.type_change)
        self.refresh_table()
        # Conectar returnPressed para buscar ao pressionar Enter
        self.search_bar.returnPressed.connect(self.search)
        self.view_properties.clicked.connect(self.register_property_action)

        # Evitar que Enter dispare botões do diálogo (como 'Ver propriedades')
        try:
            for btn in (self.view_properties, self.add, self.edit, self.delete_2):
                btn.setAutoDefault(False)
                btn.setDefault(False)
        except Exception:
            pass

    def search(self) -> None:
        """Busca solicitantes - Apenas ao pressionar Enter"""
        try:
            # Se o campo de busca estiver vazio, mostrar todos
            search_text = self.search_bar.text().strip()
            if not search_text:
                self.refresh_table()
                return
            
            db = Database()
            query_result = None
            
            if self.current_table_type == 'person':
                if self.search_parameter.currentText() == 'CPF/CNPJ':
                    cpf = ''.join(ch for ch in search_text if ch.isdigit())
                    query_result = db.get_persons(cpf=cpf)
                elif self.search_parameter.currentText() == 'Nome':
                    query_result = db.get_persons(name=search_text)
            elif self.current_table_type == 'company':
                if self.search_parameter.currentText() == 'CPF/CNPJ':
                    cnpj = ''.join(ch for ch in search_text if ch.isdigit())
                    query_result = db.get_companies(cnpj=cnpj)
                elif self.search_parameter.currentText() == 'Nome':
                    query_result = db.get_companies(company_name=search_text)
            
            db.close_connection()
            self.refresh_table(query_result=query_result)
            
        except Exception as e:
            print(f" Erro na busca: {e}")
            import traceback
            traceback.print_exc()

    def register_property_action(self) -> None:
        selected_items: list[QTableWidgetItem] = self.requester_table.selectedIndexes()
        if len(selected_items) == 0:
            widget: AlertWindow = AlertWindow("Você deve selecionar um solicitante para visualizar as propriedades.")
            widget.exec()
            return
        for data in selected_items:
            if data.row() != selected_items[0].row():
                widget: AlertWindow = AlertWindow("Você só pode visualizar as propriedades de um solicitante por vez.")
                widget.exec()
                return
        row: int = selected_items[0].row()
        id: str = self.requester_table.item(row, 0).text()
        db = Database()
        if self.current_table_type == 'person':
            requester_id: int = db.get_persons(id=id)[0]['requester_id']
        else:
            requester_id: int = db.get_companies(id=id)[0]['requester_id']
        requester: sqlite3.Row = db.get_requesters(requester_id=requester_id)[0]
        if requester['requester_type'] == 'person':
            requester_text = f"{requester_id} | {requester['name']} | CPF: {requester['document_number']}"
        else:
            requester_text = f"{requester_id} | {requester['name']} | CNPJ: {requester['document_number']}"
        dialog: PropertyWindow = PropertyWindow(owner=requester_text, owner_id = requester_id)
        dialog.exec()
        db.close_connection()

    def delete_requester(self) -> None:
        try:
            selected_items: list[QTableWidgetItem] = self.requester_table.selectedIndexes()
            if len(selected_items) == 0:
                widget: AlertWindow = AlertWindow("Você deve selecionar um solicitante para deletar.")
                widget.exec()
                return

            selected_requesters: set[int] = {selected_item.row() for selected_item in selected_items}
            list_of_ids: list[int] = [int(self.requester_table.item(item_row, 0).text()) for item_row in selected_requesters]
            dialog: DeleteConfirmation = DeleteConfirmation(list_of_ids=list_of_ids,  table_type=self.current_table_type, message="Deseja deletar todos os solicitantes selecionados?")
            dialog.exec()


        except Exception as e:
            error = handle_exception(e)
            widget: AlertWindow = AlertWindow(error)
            widget.exec()
        self.refresh_table()



    def type_change(self) -> None:
        if self.requester_type.currentText() == 'Pessoa física':
            self.create_person_table()
            self.add.clicked.disconnect(self.register_company)
            self.add.clicked.connect(self.register_person)
            self.current_table_type = 'person'
        elif self.requester_type.currentText() == 'Pessoa jurídica':
            self.create_company_table()
            self.add.clicked.disconnect(self.register_person)
            self.add.clicked.connect(self.register_company)
            self.current_table_type = 'company'


    def edit_requester(self) -> None:
        """Edita solicitante - VERSÃO SEGURA"""
        try:
            selected_items = self.requester_table.selectedIndexes()
            
            if not selected_items:
                from interface.AlertWindow import AlertWindow
                AlertWindow("Selecione um solicitante para editar.").exec()
                return
            
            # Verificar se só uma linha está selecionada
            rows = {item.row() for item in selected_items}
            if len(rows) > 1:
                from interface.AlertWindow import AlertWindow
                AlertWindow("Selecione apenas um solicitante por vez.").exec()
                return
            
            row = list(rows)[0]
            id_str = self.requester_table.item(row, 0).text()
            
            if not id_str:
                print("  ID não encontrado na tabela")
                return
            
            try:
                requester_id = int(id_str)
            except ValueError:
                print(f"  ID inválido: {id_str}")
                return
            
            db = Database()
            
            if self.current_table_type == 'person':
                # Usar método get_persons com id
                persons = db.get_persons(id=requester_id)
                if not persons:
                    print(f"  Pessoa com ID {requester_id} não encontrada")
                    db.close_connection()
                    return
                
                requester = persons[0]
                from interface.RegisterPerson import RegisterPerson
                dialog = RegisterPerson()
                
            else:  # company
                # Buscar empresa com id
                companies = db.get_companies(id=requester_id)
                if not companies:
                    print(f"  Empresa com ID {requester_id} não encontrada")
                    db.close_connection()
                    return
                
                requester = companies[0]
                from interface.RegisterCompany import RegisterCompany
                dialog = RegisterCompany()
            
            db.close_connection()
            
            # Verificar se o dialog tem método edit_mode
            if hasattr(dialog, 'edit_mode'):
                dialog.edit_mode(requester)
            else:
                print(f"  Dialog não tem método edit_mode")
            
            dialog.exec()
            self.refresh_table()
            
        except Exception as e:
            print(f" Erro ao editar solicitante: {e}")
            import traceback
            traceback.print_exc()
            from interface.AlertWindow import AlertWindow
            AlertWindow(f"Erro ao editar: {str(e)}").exec()



    def create_person_table(self) -> None:
        if self.current_table_type == 'company':
            self.requester_table.setRowCount(0)
            self.requester_table.setColumnCount(7)
            self.requester_table.setHorizontalHeaderItem(2, QTableWidgetItem("Nascimento"))
            self.requester_table.setHorizontalHeaderItem(3, QTableWidgetItem("CPF"))
            self.requester_table.setHorizontalHeaderItem(4, QTableWidgetItem("Telefone"))
            self.requester_table.setHorizontalHeaderItem(5, QTableWidgetItem("E-mail"))
            self.requester_table.setHorizontalHeaderItem(6, QTableWidgetItem("Endereço"))
            self.current_table_type = 'person'
            self.refresh_table()

    def create_company_table(self) -> None:
        if self.current_table_type == 'person':
            self.requester_table.setRowCount(0)
            self.requester_table.setColumnCount(6)
            self.requester_table.setHorizontalHeaderItem(2, QTableWidgetItem("CNPJ"))
            self.requester_table.setHorizontalHeaderItem(3, QTableWidgetItem("Telefone"))
            self.requester_table.setHorizontalHeaderItem(4, QTableWidgetItem("E-mail"))
            self.requester_table.setHorizontalHeaderItem(5, QTableWidgetItem("Endereço"))
            self.current_table_type = 'company'
            self.refresh_table()

    def refresh_table(self, **kwargs) -> None:
        db = Database()

        def _safe_id(item) -> int:
            try:
                return int(item.get('id', 0))
            except Exception:
                return 0
        
        try:
            if self.current_table_type == 'person':
                if kwargs.get('query_result') is None:
                    persons: list = db.get_persons()
                else:
                    persons: list = kwargs.get('query_result')

                persons = sorted(persons or [], key=_safe_id, reverse=True)
                
                print(f"🔍 Total de pessoas: {len(persons) if persons else 0}")
                
                self.requester_table.setRowCount(0)
                self.requester_table.setColumnCount(7)
                
                # Definir headers para tabela de pessoas
                self.requester_table.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
                self.requester_table.setHorizontalHeaderItem(1, QTableWidgetItem("Nome"))
                self.requester_table.setHorizontalHeaderItem(2, QTableWidgetItem("Nascimento"))
                self.requester_table.setHorizontalHeaderItem(3, QTableWidgetItem("CPF"))
                self.requester_table.setHorizontalHeaderItem(4, QTableWidgetItem("Telefone"))
                self.requester_table.setHorizontalHeaderItem(5, QTableWidgetItem("E-mail"))
                self.requester_table.setHorizontalHeaderItem(6, QTableWidgetItem("Endereço"))
                
                if persons:
                    for person in persons:
                        row_position: int = self.requester_table.rowCount()
                        self.requester_table.insertRow(row_position)
                        
                        # Preencher tabela com valores seguros
                        self.requester_table.setItem(row_position, 0, QTableWidgetItem(str(person.get('id', ''))))
                        self.requester_table.setItem(row_position, 1, QTableWidgetItem(person.get('name', '')))
                        self.requester_table.setItem(row_position, 2, QTableWidgetItem(person.get('birth_date', '')))
                        self.requester_table.setItem(row_position, 3, QTableWidgetItem(person.get('cpf', '')))
                        self.requester_table.setItem(row_position, 4, QTableWidgetItem(person.get('phone_number', '')))
                        self.requester_table.setItem(row_position, 5, QTableWidgetItem(person.get('email', '')))
                        
                        # Endereço formatado
                        endereco_text = self._format_address(person)
                        self.requester_table.setItem(row_position, 6, QTableWidgetItem(endereco_text))
                
            elif self.current_table_type == 'company':
                if kwargs.get('query_result') is None:
                    companies: list = db.get_companies()
                else:
                    companies: list = kwargs.get('query_result')

                companies = sorted(companies or [], key=_safe_id, reverse=True)
                
                print(f" Total de empresas: {len(companies) if companies else 0}")
                
                self.requester_table.setRowCount(0)
                self.requester_table.setColumnCount(6)
                
                # Definir headers para tabela de empresas
                self.requester_table.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
                self.requester_table.setHorizontalHeaderItem(1, QTableWidgetItem("Nome"))
                self.requester_table.setHorizontalHeaderItem(2, QTableWidgetItem("CNPJ"))
                self.requester_table.setHorizontalHeaderItem(3, QTableWidgetItem("Telefone"))
                self.requester_table.setHorizontalHeaderItem(4, QTableWidgetItem("E-mail"))
                self.requester_table.setHorizontalHeaderItem(5, QTableWidgetItem("Endereço"))
                
                if companies:
                    for company in companies:
                        row_position = self.requester_table.rowCount()
                        self.requester_table.insertRow(row_position)
                        
                        self.requester_table.setItem(row_position, 0, QTableWidgetItem(str(company.get('id', ''))))
                        self.requester_table.setItem(row_position, 1, QTableWidgetItem(company.get('company_name', '')))
                        self.requester_table.setItem(row_position, 2, QTableWidgetItem(company.get('cnpj', '')))
                        self.requester_table.setItem(row_position, 3, QTableWidgetItem(company.get('phone_number', '')))
                        self.requester_table.setItem(row_position, 4, QTableWidgetItem(company.get('email', '')))
                        
                        # Endereço formatado
                        endereco_text = self._format_address(company)
                        self.requester_table.setItem(row_position, 5, QTableWidgetItem(endereco_text))
            
            # Ajustar tamanho das colunas
            if self.requester_table.rowCount() == 0:
                self.requester_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            else:
                self.requester_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
                
        except Exception as e:
            print(f" Erro ao atualizar tabela: {e}")
            import traceback
            traceback.print_exc()
            
            # Mostrar mensagem de erro
            from interface.AlertWindow import AlertWindow
            widget = AlertWindow(f"Erro ao carregar dados: {str(e)}")
            widget.exec()
            
        finally:
            db.close_connection()

    def _format_address(self, data: dict) -> str:
        """Formata endereço de forma segura"""
        try:
            parts = []
            
            # Adicionar rua e número se existirem
            street = data.get('street', '')
            number = data.get('address_number', '')
            
            if street or number:
                if street and number:
                    parts.append(f"{street}, {number}")
                elif street:
                    parts.append(street)
                elif number:
                    parts.append(f"Nº {number}")
            
            # Adicionar CEP se existir
            cep = data.get('cep', '')
            if cep:
                parts.append(f"CEP: {cep}")
            
            # Adicionar cidade e estado
            city = data.get('city', '')
            state = data.get('state', '')
            
            if city or state:
                if city and state:
                    parts.append(f"{city}/{state}")
                elif city:
                    parts.append(city)
                elif state:
                    parts.append(state)
            
            # Adicionar país se não for Brasil
            country = data.get('country', 'Brasil')
            if country and country != 'Brasil':
                parts.append(country)
            
            return " - ".join(parts) if parts else "Endereço não informado"
            
        except Exception as e:
            print(f"  Erro ao formatar endereço: {e}")
            return "Endereço não disponível"


    def register_person(self) -> None:
        dialog: RegisterPerson = RegisterPerson()
        dialog.exec()
        self.refresh_table()

    def register_company(self) -> None:
        dialog: RegisterCompany = RegisterCompany()
        dialog.exec()
        self.refresh_table()

    def register_property_action(self) -> None:
        """Visualiza propriedades - VERSÃO SIMPLIFICADA"""
        try:
            selected_items = self.requester_table.selectedIndexes()
            
            if not selected_items:
                from interface.AlertWindow import AlertWindow
                AlertWindow("Selecione um solicitante.").exec()
                return
            
            # Pegar a primeira linha selecionada
            row = selected_items[0].row()
            id_str = self.requester_table.item(row, 0).text()
            name = self.requester_table.item(row, 1).text()
            
            if self.current_table_type == 'person':
                cpf_cnpj = self.requester_table.item(row, 3).text()
                requester_text = f"{id_str} | {name} | CPF: {cpf_cnpj}"
            else:
                cnpj = self.requester_table.item(row, 2).text()
                requester_text = f"{id_str} | {name} | CNPJ: {cnpj}"
            
            try:
                requester_id = int(id_str)
            except ValueError:
                print(f"  ID inválido: {id_str}")
                return
            
            from interface.PropertyWindow import PropertyWindow
            dialog = PropertyWindow(owner=requester_text, owner_id=requester_id)
            dialog.exec()
            
        except Exception as e:
            print(f" Erro ao visualizar propriedades: {e}")
            import traceback
            traceback.print_exc()
