from PySide6.QtWidgets import (QDialog, QCompleter, QTableWidgetItem)
from base_windows.property_window import PropertyDialog
from PySide6.QtCore import Qt
from ErrorWindow import ErrorWindow
from DeleteConfirmation import DeleteConfirmation
from SucessfulRegister import SucessfulRegister
from backend.classes.utils import handle_exception
from RegisterProperty import RegisterProperty
from backend.classes.Database import Database
from SampleWindow import SampleWindow
import sqlite3

class PropertyWindow(QDialog, PropertyDialog):
    def __init__(self, **kwargs) -> None:
        super(PropertyWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Propriedades cadastradas')
        self.requester_list: list[sqlite3.Row] | None = None
        self.current_owner: str = kwargs.get('owner') if kwargs.get('owner') else ''
        self.owner.setText(self.current_owner)
        self.owner.setReadOnly(True)
        self.current_owner_id = kwargs.get('owner_id')
        self.add.clicked.connect(self.register_property)
        self.edit.clicked.connect(self.edit_property)
        self.delete_2.clicked.connect(self.delete_property)
        self.view_samples.clicked.connect(self.open_sample_widget)
        self.refresh_table()

    def refresh_table(self) -> None:
        db: Database = Database()
        properties: list[sqlite3.Row] = db.get_properties(requester_id=self.current_owner_id)
        self.property_table.setRowCount(0)
        for property in properties:
            row_position: int = self.property_table.rowCount()
            self.property_table.insertRow(row_position)
            self.property_table.setItem(row_position, 0, QTableWidgetItem(str(property['id'])))
            self.property_table.setItem(row_position, 1, QTableWidgetItem(property['name']))
            self.property_table.setItem(row_position, 2, QTableWidgetItem(
                f"{property['location']}, {property['city']} - {property['state']}, {property['country']}"))
            self.property_table.setItem(row_position, 3, QTableWidgetItem(str(property['registration_number'])))

    def register_property(self) -> None:
        dialog: RegisterProperty = RegisterProperty(self.current_owner_id)
        dialog.exec()
        self.refresh_table()

    def edit_property(self) -> None:
        dialog: RegisterProperty = RegisterProperty(self.current_owner_id)
        selected_items: list[QTableWidgetItem] = self.property_table.selectedIndexes()
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
        id: str = self.property_table.item(row, 0).text()
        db: Database = Database()
        property: sqlite3.Row = db.get_properties(id=id)[0]
        db.close_connection()
        dialog.edit_mode(property)
        dialog.exec()
        self.refresh_table()

    def delete_property(self) -> None:
        try:
            selected_items: list[QTableWidgetItem] = self.property_table.selectedIndexes()
            if len(selected_items) == 0:
                widget: ErrorWindow = ErrorWindow("Você deve selecionar ao menos uma propriedade para deletar.")
                widget.exec()
                return
            selected_properties: set[int] = {selected_item.row() for selected_item in selected_items}
            list_of_ids: list[int] = [int(self.property_table.item(item_row, 0).text()) for item_row in selected_properties]
            dialog: DeleteConfirmation = DeleteConfirmation(list_of_ids=list_of_ids, table_type="property", message="Deseja deletar todos as propriedades selecionadas?")
            dialog.exec()
            sucessful_dialog: SucessfulRegister = SucessfulRegister(sucess_message="Propriedade deletada com sucesso!")
            sucessful_dialog.exec()
        except Exception as e:
            error = handle_exception(e)
            widget: ErrorWindow = ErrorWindow(error)
            widget.exec()
        self.refresh_table()

    def open_sample_widget(self) -> None:
        selected_items: list[QTableWidgetItem] = self.property_table.selectedIndexes()
        if len(selected_items) == 0:
            widget: ErrorWindow = ErrorWindow("Você deve selecionar uma propriedade para ver as amostras.")
            widget.exec()
            return
        for data in selected_items:
            if data.row() != selected_items[0].row():
                widget: ErrorWindow = ErrorWindow("Você só pode ver as amostras de uma propriedade por vez.")
                widget.exec()
                return
        widget: SampleWindow = SampleWindow(owner=self.owner.text(), owner_id=self.current_owner_id,
                                            property=self.property_table.item(selected_items[0].row(), 1).text(),
                                            property_id = int(self.property_table.item(selected_items[0].row(), 0).text()))
        widget.exec()