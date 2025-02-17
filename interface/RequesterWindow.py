import os

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (QDialog, QTableWidgetItem, QAbstractItemView, QHeaderView)
from interface.base_windows.requester_window import RequesterDialog
from interface.DeleteConfirmation import DeleteConfirmation
from interface.AlertWindow import AlertWindow
from backend.classes.utils import handle_exception
from interface.RegisterCompany import RegisterCompany
from interface.RegisterPerson import RegisterPerson
from backend.classes.Database import Database
from interface.PropertyWindow import PropertyWindow
import sqlite3


class RequesterWindow(QDialog, RequesterDialog):
    def __init__(self) -> None:
        super(RequesterWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Solicitantes registrados')
        self.setWindowIcon(QPixmap(os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "interface",
            "images"
        ).replace("\\", "/") + "/GAIA_icon.png"))
        self.requester_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.add.clicked.connect(self.register_person)
        self.edit.clicked.connect(self.edit_requester)
        self.delete_2.clicked.connect(self.delete_requester)
        self.current_table_type = 'person'
        self.requester_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.requester_type.currentTextChanged.connect(self.type_change)
        self.refresh_table()
        self.search_bar.textEdited.connect(self.search)
        self.view_properties.clicked.connect(self.register_property_action)

    def search(self) -> None:
        db: Database = Database()
        if self.search_parameter.currentText() == 'CPF/CNPJ' and self.current_table_type == 'person':
            query_result: list[sqlite3.Row] = db.get_persons(cpf=self.search_bar.text())
        elif self.search_parameter.currentText() == 'Nome' and self.current_table_type == 'person':
            query_result: list[sqlite3.Row] = db.get_persons(name=self.search_bar.text())
        elif self.search_parameter.currentText() == 'CPF/CNPJ' and self.current_table_type == 'company':
            query_result: list[sqlite3.Row] = db.get_companies(cnpj=self.search_bar.text())
        elif self.search_parameter.currentText() == 'Nome' and self.current_table_type == 'company':
            query_result: list[sqlite3.Row] = db.get_companies(company_name=self.search_bar.text())
        db.close_connection()
        self.refresh_table(query_result=query_result)

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
        db: Database = Database()
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
        dialog: RegisterPerson | RegisterCompany = RegisterPerson() if self.current_table_type == 'person' else RegisterCompany()
        selected_items: list[QTableWidgetItem] = self.requester_table.selectedIndexes()

        if len(selected_items) == 0:
            widget: AlertWindow = AlertWindow("Você deve selecionar um solicitante para editar.")
            widget.exec()
            return

        for data in selected_items:
            if data.row() != selected_items[0].row():
                widget: AlertWindow = AlertWindow("Você só pode editar um solicitante por vez.")
                widget.exec()
                return

        row: int = selected_items[0].row()
        id: str = self.requester_table.item(row, 0).text()
        db: Database = Database()
        requesters = db.get_persons(id=id) if self.current_table_type == 'person' else db.get_companies(id=id)
        requester = requesters[0]
        db.close_connection()

        dialog.edit_mode(requester)
        dialog.exec()
        self.refresh_table()



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
        db: Database = Database()
        if self.current_table_type == 'person':
            if kwargs.get('query_result') is None:
                persons: list[sqlite3.Row] = db.get_persons()
            else:
                persons: list[sqlite3.Row] = kwargs.get('query_result')
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
        elif self.current_table_type == 'company':
            if kwargs.get('query_result') is None:
                companies: list[sqlite3.Row] = db.get_companies()
            else:
                companies: list[sqlite3.Row] = kwargs.get('query_result')
            self.requester_table.setRowCount(0)
            for company in companies:
                row_position = self.requester_table.rowCount()
                self.requester_table.insertRow(row_position)
                self.requester_table.setItem(row_position, 0, QTableWidgetItem(str(company['id'])))
                self.requester_table.setItem(row_position, 1, QTableWidgetItem(company['company_name']))
                self.requester_table.setItem(row_position, 2, QTableWidgetItem(company['cnpj']))
                self.requester_table.setItem(row_position, 3, QTableWidgetItem(company['phone_number']))
                self.requester_table.setItem(row_position, 4, QTableWidgetItem(company['email']))
                self.requester_table.setItem(row_position, 5, QTableWidgetItem(f"{company['street']}, {company['address_number']} - {company['cep']}, {company['city']}, {company['state']}, {company['country']}"))
        if self.requester_table.rowCount() == 0:
            self.requester_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        else:
            self.requester_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        db.close_connection()


    def register_person(self) -> None:
        dialog: RegisterPerson = RegisterPerson()
        dialog.exec()
        self.refresh_table()

    def register_company(self) -> None:
        dialog: RegisterCompany = RegisterCompany()
        dialog.exec()
        self.refresh_table()
