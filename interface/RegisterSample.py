from PySide6.QtWidgets import (QDialog, QCompleter)
from interface.base_windows.register_sample import RegisterSampleDialog
from PySide6.QtCore import Qt
from backend.classes.Database import Database
from backend.classes.Sample import Sample
from interface.ErrorWindow import ErrorWindow
from interface.SucessfulRegister import SucessfulRegister
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

    def edit_mode(self, sample_data) -> None:
        self.sample_number.clear()
        self.sample_number.insert(str(sample_data["sample_number"]))
        self.collection_depth.insert(str(sample_data["depth"]))
        self.date.insert(sample_data["collection_date"])
        self.description.insert(sample_data["description"])
        self.area.insert(str(sample_data["total_area"]))
        self.latitude.insert(str(sample_data["latitude"]))
        self.longitude.insert(str(sample_data["longitude"]))
        self.phosphorus.insert(str(sample_data["phosphorus"]))
        self.potassium.insert(str(sample_data["potassium"]))
        self.organic_matter.insert(str(sample_data["organic_matter"]))
        self.ph.insert(str(sample_data["ph"]))
        self.SMP.insert(str(sample_data["smp"]))
        self.read_aluminum.insert(str(sample_data["aluminum"]))
        self.read_calcium.insert(str(sample_data["calcium"]))
        self.read_magnesium.insert(str(sample_data["magnesium"]))
        self.read_copper.insert(str(sample_data["copper"]))
        self.read_iron.insert(str(sample_data["iron"]))
        self.read_manganese.insert(str(sample_data["manganese"]))
        self.read_zinc.insert(str(sample_data["zinc"]))
        self.blank_test_aluminum.insert('0')
        self.blank_test_calcium.insert('0')
        self.blank_test_magnesium.insert('0')
        self.blank_test_copper.insert('0')
        self.blank_test_iron.insert('0')
        self.blank_test_manganese.insert('0')
        self.blank_test_zinc.insert('0')
        self.register_button.setText("Salvar alterações")
        self.setWindowTitle('Edição de registro de amostra')
        self.mode = 'edit'
        self.current_sample_id = int(sample_data['id'])

    def register_action(self) -> None:
        db: Database = Database()
        sample: Sample = Sample(depth=float(self.collection_depth.text()), collection_date=self.date.text(),
                                description=self.description.text(), total_area=float(self.area.text()),
                                latitude=float(self.latitude.text()), longitude=float(self.longitude.text()),
                                phosphorus=float(self.phosphorus.text()), potassium=float(self.potassium.text()),
                                organic_matter=float(self.organic_matter.text()), ph=float(self.ph.text()),
                                smp=float(self.SMP.text()),
                                aluminum=float(self.read_aluminum.text()) - float(self.blank_test_aluminum.text()),
                                calcium=float(self.read_calcium.text()) - float(self.blank_test_calcium.text()),
                                magnesium=float(self.read_magnesium.text()) - float(self.blank_test_magnesium.text()),
                                copper=float(self.read_copper.text()) - float(self.blank_test_copper.text()),
                                iron=float(self.read_iron.text()) - float(self.blank_test_iron.text()),
                                manganese=float(self.read_manganese.text()) - float(self.blank_test_manganese.text()),
                                zinc=float(self.read_zinc.text()) - float(self.blank_test_zinc.text()))
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
