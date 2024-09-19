from backend.classes.Database import Database
from base_windows.delete_confirmation import DeleteDialog
from PySide6.QtWidgets import (QDialog)

class DeleteConfirmation(QDialog, DeleteDialog):
    def __init__(self, list_of_ids: list[int], requester_type: str) -> None:
        super(DeleteConfirmation, self).__init__()  # Initialize QDialog properly
        self.setupUi(self)
        self.confirm_button.clicked.connect(self.delete_action)
        self.cancel_button.clicked.connect(self.close)

        # Store the additional parameters
        self.list_of_ids = list_of_ids
        self.requester_type = requester_type

    def delete_action(self) -> None:
        db: Database = Database()
        for id in self.list_of_ids:
            if self.requester_type == 'person':
                db.delete_person(id)
            elif self.requester_type == 'company':
                db.delete_company(id)
        db.close_connection()
        self.close()