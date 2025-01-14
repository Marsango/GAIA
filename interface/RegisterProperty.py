import os

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (QDialog, QCompleter)
from interface.base_windows.register_property import RegisterPropertyDialog
from PySide6.QtCore import Qt
from backend.classes.Database import Database
from backend.classes.Property import Property
from interface.AlertWindow import AlertWindow
from backend.classes.utils import handle_exception


class RegisterProperty(QDialog, RegisterPropertyDialog):
    def __init__(self, requester_id: int) -> None:
        super(RegisterProperty, self).__init__()
        self.current_property_id: int | None = None
        self.setupUi(self)
        self.setWindowTitle('Registro de propriedade')
        self.setWindowIcon(QPixmap(os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "interface",
            "images"
        ).replace("\\", "/") + "/logo_lab.png"))
        self.register_button.clicked.connect(self.register_action)
        self.create_country_completer()
        self.country_input.editingFinished.connect(self.country_changed)
        self.state_input.editingFinished.connect(self.state_changed)
        self.requester_id: int = requester_id
        self.mode: str = 'register'

    def edit_mode(self, property_data) -> None:
        self.country_input.insert(property_data['country'])
        self.state_input.insert(property_data['state'])
        self.city_input.insert(property_data['city'])
        self.name_input.insert(property_data['name'])
        self.registration_number_input.insert(str(property_data['registration_number']))
        self.location_input.insert(property_data['location'])

        self.register_button.setText("Salvar alterações")
        self.setWindowTitle('Edição de registro de propriedade')
        self.mode = 'edit'
        self.current_property_id = int(property_data['id'])

    def create_country_completer(self) -> None:
        db: Database = Database()
        completer: QCompleter = QCompleter(db.get_countries(), self)
        db.close_connection()
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.country_input.setCompleter(completer)

    def country_changed(self) -> None:
        db: Database = Database()
        completer: QCompleter = QCompleter(db.get_states(self.country_input.text()), self)
        db.close_connection()
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.state_input.setCompleter(completer)

    def state_changed(self) -> None:
        db: Database = Database()
        completer: QCompleter = QCompleter(db.get_cities(self.state_input.text()), self)
        db.close_connection()
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.city_input.setCompleter(completer)


    def register_action(self) -> None:
        db: Database = Database()
        try:
            property: Property = Property(name=self.name_input.text(), country=self.country_input.text(),
                                          state=self.state_input.text(), city=self.city_input.text(),
                                          location = self.location_input.text(),
                                          registration_number=self.registration_number_input.text())
            if self.mode == 'register':
                db.insert_property(property, self.requester_id)
                success: str = "Propriedade registrada com sucesso!"
            else:
                db.edit_property(property, self.current_property_id)
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