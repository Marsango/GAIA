from PySide6.QtWidgets import (QDialog, QCompleter)
from base_windows.register_sample import RegisterSampleDialog
from PySide6.QtCore import Qt
from backend.classes.Database import Database
from backend.classes.Sample import Sample
from ErrorWindow import ErrorWindow
from SucessfulRegister import SucessfulRegister
from backend.classes.utils import handle_exception


class RegisterSample(QDialog, RegisterSampleDialog):
    def __init__(self, property_id: int, sample_number: int) -> None:
        super(RegisterSample, self).__init__()
        self.current_property_id: int = property_id
        self.current_sample_id: int | None = None
        self.setupUi(self)
        self.setWindowTitle('Registro de amostra')
        self.register_button.clicked.connect(self.register_action)
        self.mode: str = 'register'
        self.sample_number.setReadOnly(True)
        self.sample_number.setText(str(sample_number))

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


    def register_action(self) -> None:
        db: Database = Database()
        sample: Sample = Sample(depth=float(self.collection_depth.text()), collection_date=self.date.text(),
                                description=self.description.text(), total_area=float(self.area.text()),
                                latitude=float(self.latitude.text()), longitude=float(self.longitude.text()),
                                phosphorus=float(self.phosphorus.text()), potassium=float(self.potassium.text()),
                                organic_matter=float(self.organic_matter.text()), ph=float(self.ph.text()),
                                smp=float(self.SMP.text()), h_al=float(self.h_plus_al.text()),
                                aluminum=float(self.read_aluminum.text()) - float(self.blank_test_aluminum.text()),
                                calcium=float(self.read_calcium.text()) - float(self.blank_test_calcium.text()),
                                magnesium=float(self.read_magnesium.text()) - float(self.blank_test_magnesium.text()),
                                copper=float(self.read_copper.text()) - float(self.blank_test_copper.text()),
                                iron=float(self.read_iron.text()) - float(self.blank_test_iron.text()),
                                manganese=float(self.read_manganese.text()) - float(self.blank_test_manganese.text()),
                                zinc = float(self.read_zinc.text()) - float(self.blank_test_zinc.text()))
        if self.mode == 'register':
            db.insert_sample(sample, self.current_property_id, int(self.sample_number.text()))
            sucess_text: str = "Amostra registrada com sucesso!"
        elif self.mode == 'edit':
            db.edit_sample(sample, self.current_sample_id)
            sucess_text: str = "Alterações salvas com sucesso!"
        widget: SucessfulRegister = SucessfulRegister(sucess_message=sucess_text)
        widget.exec()
        if self.mode == 'register':
            self.clean_input()
        # except Exception as e:
        #     error = handle_exception(e)
        #     widget: ErrorWindow = ErrorWindow(error)
        #     widget.exec()
        db.close_connection()

    def clean_input(self):
        self.collection_depth.clear()
        self.date.clear()
        self.description.clear()
        self.area.clear()
        self.latitude.clear()
        self.longitude.clear()
        self.phosphorus.clear()
        self.potassium.clear()
        self.organic_matter.clear()
        self.ph.clear()
        self.SMP.clear()
        self.h_plus_al.clear()
        self.read_aluminum.clear()
        self.blank_test_aluminum.clear()
        self.read_calcium.clear()
        self.blank_test_calcium.clear()
        self.read_magnesium.clear()
        self.blank_test_magnesium.clear()
        self.read_copper.clear()
        self.blank_test_copper.clear()
        self.read_iron.clear()
        self.blank_test_iron.clear()
        self.read_manganese.clear()
        self.blank_test_manganese.clear()
        self.read_zinc.clear()
        self.blank_test_zinc.clear()
