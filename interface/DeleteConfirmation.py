from backend.classes.Database import Database
from interface.base_windows.delete_confirmation import DeleteDialog
from PySide6.QtWidgets import (QDialog)

class DeleteConfirmation(QDialog, DeleteDialog):
    def __init__(self, list_of_ids: list[int], table_type: str, **kwargs) -> None:
        super(DeleteConfirmation, self).__init__()
        self.setupUi(self)
        self.confirm_button.clicked.connect(self.delete_action)
        self.cancel_button.clicked.connect(self.close)
        self.list_of_ids: list[int] = list_of_ids
        self.table_type: str = table_type
        message = kwargs.get('message')
        if message:
            self.label.setText(f"<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">{message}</span></p></body></html>")

    def delete_action(self) -> None:
        db: Database = Database()
        for id in self.list_of_ids:
            if self.table_type == 'person':
                db.delete_person(id)
            elif self.table_type == 'company':
                db.delete_company(id)
            elif self.table_type == 'property':
                db.delete_property(id)
            elif self.table_type == 'sample':
                db.delete_sample(id)
        db.close_connection()
        self.close()

