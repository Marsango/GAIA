from PySide6.QtWidgets import (QDialog, QTableWidgetItem, QAbstractItemView, QHeaderView)
from interface.base_windows.sample_window import SampleDialog
from interface.ErrorWindow import ErrorWindow
from interface.DeleteConfirmation import DeleteConfirmation
from interface.SucessfulRegister import SucessfulRegister
from backend.classes.utils import handle_exception
from backend.classes.Database import Database
from interface.RegisterSample import RegisterSample
from interface.GenerateReport import GenerateReport
import sqlite3


class SampleWindow(QDialog, SampleDialog):
    def __init__(self, **kwargs) -> None:
        super(SampleWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Amostras cadastradas')
        owner: str = kwargs.get('owner') if kwargs.get('owner') else ''
        _property: str = kwargs.get('property') if kwargs.get('property') else ''
        self.owner.setText(owner)
        self.owner.setReadOnly(True)
        self._property.setText(_property)
        self._property.setReadOnly(True)
        self.sample_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.sample_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.sample_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.sample_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.current_owner_id: int = kwargs.get('owner_id')
        self.current_property_id: int = kwargs.get('property_id')
        self.add.clicked.connect(self.register_sample)
        self.edit.clicked.connect(self.edit_sample)
        self.delete_2.clicked.connect(self.delete_sample)
        self.refresh_table()
        self.generate_report.clicked.connect(self.report_window)

    def refresh_table(self) -> None:
        db: Database = Database()
        samples: list[sqlite3.Row] = db.get_samples(property_id=self.current_property_id)
        self.sample_table.setRowCount(0)
        for sample in samples:
            row_position: int = self.sample_table.rowCount()
            self.sample_table.insertRow(row_position)
            self.sample_table.setItem(row_position, 0, QTableWidgetItem(str(sample['id'])))
            self.sample_table.setItem(row_position, 1, QTableWidgetItem(str(sample['sample_number'])))
            self.sample_table.setItem(row_position, 2, QTableWidgetItem(sample['description']))
            self.sample_table.setItem(row_position, 3, QTableWidgetItem(str(sample['depth'])))
            self.sample_table.setItem(row_position, 4, QTableWidgetItem(str(sample['collection_date'])))

    def register_sample(self) -> None:
        dialog: RegisterSample = RegisterSample(self.current_property_id, self.sample_table.rowCount() + 1)
        dialog.exec()
        self.refresh_table()

    def edit_sample(self) -> None:
        dialog: RegisterSample = RegisterSample(self.current_property_id, self.sample_table.rowCount() + 1)
        selected_items: list[QTableWidgetItem] = self.sample_table.selectedIndexes()
        if len(selected_items) == 0:
            widget: ErrorWindow = ErrorWindow("Você deve selecionar uma amostra para editar.")
            widget.exec()
            return
        for data in selected_items:
            if data.row() != selected_items[0].row():
                widget: ErrorWindow = ErrorWindow("Você só pode editar uma amostra por vez.")
                widget.exec()
                return
        row: int = selected_items[0].row()
        id: str = self.sample_table.item(row, 0).text()
        db: Database = Database()
        sample: sqlite3.Row = db.get_samples(id=id)[0]
        db.close_connection()
        dialog.edit_mode(sample)
        dialog.exec()
        self.refresh_table()

    def delete_sample(self) -> None:
        try:
            selected_items: list[QTableWidgetItem] = self.sample_table.selectedIndexes()
            if len(selected_items) == 0:
                widget: ErrorWindow = ErrorWindow("Você deve selecionar ao menos uma amostra para deletar.")
                widget.exec()
                return
        
            selected_samples: set[int] = {selected_item.row() for selected_item in selected_items}
            list_of_ids: list[int] = [int(self.sample_table.item(item_row, 0).text()) for item_row in selected_samples]

            dialog: DeleteConfirmation = DeleteConfirmation(list_of_ids=list_of_ids, table_type="sample", message="Deseja deletar todas as amostras selecionadas?")
            if dialog.exec() == QDialog.Accepted:  # Só deletar se o usuário confirmar
                db: Database = Database()

                # Deletar solicitantes da base de dados
                for requester_id in list_of_ids:
                    if self.current_table_type == 'sample':
                        db.delete_sample(requester_id)

                db.close_connection()

                # Exibir diálogo de sucesso
                sucessful_dialog: SucessfulRegister = SucessfulRegister(sucess_message="Solicitante deletado com sucesso!")
                sucessful_dialog.exec()

        except Exception as e:
            error = handle_exception(e)
            widget: ErrorWindow = ErrorWindow(error)
            widget.exec()
        self.refresh_table()

    def report_window(self):
        selected_items: list[QTableWidgetItem] = self.sample_table.selectedIndexes()
        if len(selected_items) == 0:
            widget: ErrorWindow = ErrorWindow("Você deve selecionar uma amostra para gerar um laudo.")
            widget.exec()
            return
        for data in selected_items:
            if data.row() != selected_items[0].row():
                widget: ErrorWindow = ErrorWindow("Você gerar laudo de uma amostra por vez.")
                widget.exec()
                return
        row: int = selected_items[0].row()
        sample_id: int = int(self.sample_table.item(row, 0).text())
        dialog: GenerateReport = GenerateReport(sample_id)
        dialog.exec()