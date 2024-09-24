from PySide6.QtWidgets import (QDialog, QCompleter)
from base_windows.property_window import PropertyDialog
from PySide6.QtCore import Qt
from ErrorWindow import ErrorWindow
from DeleteConfirmation import DeleteConfirmation
from SucessfulRegister import SucessfulRegister
from backend.classes.utils import handle_exception
from RegisterCompany import RegisterCompany
from RegisterPerson import RegisterPerson
from backend.classes.Database import Database
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


    def update_property_list(self) -> None:
        db: Database




