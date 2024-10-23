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

        try:
            # Verifica se os campos obrigatórios estão preenchidos
            if not self.collection_depth.text() or not self.area.text() or not self.latitude.text() or not self.longitude.text():
                raise ValueError("Por favor, preencha todos os campos obrigatórios.")
            
            # Tenta converter os valores para float, se o campo estiver vazio, atribui 0.0
            depth = float(self.collection_depth.text()) if self.collection_depth.text() != '' else 0.0
            total_area = float(self.area.text()) if self.area.text() != '' else 0.0
            latitude = float(self.latitude.text()) if self.latitude.text() != '' else 0.0
            longitude = float(self.longitude.text()) if self.longitude.text() != '' else 0.0
            phosphorus = float(self.phosphorus.text()) if self.phosphorus.text() != '' else 0.0
            potassium = float(self.potassium.text()) if self.potassium.text() != '' else 0.0
            organic_matter = float(self.organic_matter.text()) if self.organic_matter.text() != '' else 0.0
            ph = float(self.ph.text()) if self.ph.text() != '' else 0.0
            smp = float(self.SMP.text()) if self.SMP.text() != '' else 0.0
            aluminum = float(self.read_aluminum.text()) if self.read_aluminum.text() != '' else 0.0
            blank_aluminum = float(self.blank_test_aluminum.text()) if self.blank_test_aluminum.text() != '' else 0.0
            calcium = float(self.read_calcium.text()) if self.read_calcium.text() != '' else 0.0
            blank_calcium = float(self.blank_test_calcium.text()) if self.blank_test_calcium.text() != '' else 0.0
            magnesium = float(self.read_magnesium.text()) if self.read_magnesium.text() != '' else 0.0
            blank_magnesium = float(self.blank_test_magnesium.text()) if self.blank_test_magnesium.text() != '' else 0.0
            copper = float(self.read_copper.text()) if self.read_copper.text() != '' else 0.0
            blank_copper = float(self.blank_test_copper.text()) if self.blank_test_copper.text() != '' else 0.0
            iron = float(self.read_iron.text()) if self.read_iron.text() != '' else 0.0
            blank_iron = float(self.blank_test_iron.text()) if self.blank_test_iron.text() != '' else 0.0
            manganese = float(self.read_manganese.text()) if self.read_manganese.text() != '' else 0.0
            blank_manganese = float(self.blank_test_manganese.text()) if self.blank_test_manganese.text() != '' else 0.0
            zinc = float(self.read_zinc.text()) if self.read_zinc.text() != '' else 0.0
            blank_zinc = float(self.blank_test_zinc.text()) if self.blank_test_zinc.text() != '' else 0.0

            # Criação do objeto Sample com os valores
            sample: Sample = Sample(depth=depth, collection_date=self.date.text(),
                                    description=self.description.text(), total_area=total_area,
                                    latitude=latitude, longitude=longitude,
                                    phosphorus=phosphorus, potassium=potassium,
                                    organic_matter=organic_matter, ph=ph, smp=smp,
                                    aluminum=aluminum - blank_aluminum,
                                    calcium=calcium - blank_calcium,
                                    magnesium=magnesium - blank_magnesium,
                                    copper=copper - blank_copper,
                                    iron=iron - blank_iron,
                                    manganese=manganese - blank_manganese,
                                    zinc=zinc - blank_zinc)

            # Verifica se estamos registrando ou editando
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
        except ValueError as e:
            # Mostra uma janela de erro se houver um ValueError, como campo vazio
            widget: ErrorWindow = ErrorWindow(f"Erro: {str(e)}")
            widget.exec()

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
