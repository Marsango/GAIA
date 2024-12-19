import os

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (QDialog)
from interface.base_windows.register_sample import RegisterSampleDialog
from backend.classes.Database import Database
from backend.classes.Sample import Sample
from interface.AlertWindow import AlertWindow


class RegisterSample(QDialog, RegisterSampleDialog):
    def __init__(self, property_id: int, sample_number: int) -> None:
        super(RegisterSample, self).__init__()
        self.current_property_id: int = property_id
        self.current_sample_id: int | None = None
        self.setupUi(self)
        self.setWindowTitle('Registro de amostra')
        self.setWindowIcon(QPixmap(os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "interface",
            "images"
        ).replace("\\", "/") + "/logo_lab.png"))
        self.register_button.clicked.connect(self.register_action)
        self.mode: str = 'register'

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
        self.clay_input.insert(str(sample_data["clay"]))
        self.silte_input.insert(str(sample_data["silte"]))
        self.sand_input.insert(str(sample_data["sand"]))
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
            if not self.collection_depth.text() or not self.area.text() or not self.latitude.text() or not self.longitude.text() or not self.sample_number.text():
                raise ValueError("Por favor, preencha todos os campos obrigatórios.")
            
            # Conversões com substituição para 0 caso o campo esteja vazio
            depth: float = float(self.collection_depth.text() or 0)
            total_area: float = float(self.area.text() or 0)
            latitude: float = float(self.latitude.text() or 0)
            longitude: float = float(self.longitude.text() or 0)
            sand: float | None = float(self.sand_input.text() or 0)  # Substituir valor nulo por 0
            silte: float | None = float(self.silte_input.text() or 0)  # Substituir valor nulo por 0
            clay: float | None = float(self.clay_input.text() or 0)  # Substituir valor nulo por 0
            phosphorus: float | None = float(self.phosphorus.text() or 0)  # Substituir valor nulo por 0
            potassium: float | None = float(self.potassium.text() or 0)  # Substituir valor nulo por 0
            organic_matter: float | None = float(self.organic_matter.text() or 0)  # Substituir valor nulo por 0
            ph: float | None = float(self.ph.text() or 0)  # Substituir valor nulo por 0
            smp: float | None = float(self.SMP.text() or 0)  # Substituir valor nulo por 0
            aluminum: float | None = float(self.read_aluminum.text() or 0)  # Substituir valor nulo por 0
            blank_aluminum: float | None = float(self.blank_test_aluminum.text() or 0)  # Substituir valor nulo por 0
            calcium: float | None = float(self.read_calcium.text() or 0)  # Substituir valor nulo por 0
            blank_calcium: float | None = float(self.blank_test_calcium.text() or 0)  # Substituir valor nulo por 0
            magnesium: float | None = float(self.read_magnesium.text() or 0)  # Substituir valor nulo por 0
            blank_magnesium: float | None = float(self.blank_test_magnesium.text() or 0)  # Substituir valor nulo por 0
            copper: float | None = float(self.read_copper.text() or 0)  # Substituir valor nulo por 0
            blank_copper: float | None = float(self.blank_test_copper.text() or 0)  # Substituir valor nulo por 0
            iron: float | None = float(self.read_iron.text() or 0)  # Substituir valor nulo por 0
            blank_iron: float | None = float(self.blank_test_iron.text() or 0)  # Substituir valor nulo por 0
            manganese: float | None = float(self.read_manganese.text() or 0)  # Substituir valor nulo por 0
            blank_manganese: float | None = float(self.blank_test_manganese.text() or 0)  # Substituir valor nulo por 0
            zinc: float | None = float(self.read_zinc.text() or 0)  # Substituir valor nulo por 0
            blank_zinc: float | None = float(self.blank_test_zinc.text() or 0)  # Substituir valor nulo por 0

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
                                    zinc=zinc - blank_zinc, clay=clay, sand=sand, silte=silte)
            
            if self.mode == 'register':
                db.insert_sample(sample, self.current_property_id, int(self.sample_number.text()))
                success: str = "Amostra registrada com sucesso!"
            elif self.mode == 'edit':
                db.edit_sample(sample, self.current_sample_id)
                success: str = "Alterações salvas com sucesso!"

            widget: AlertWindow = AlertWindow(message=success)
            widget.exec()

            if self.mode == 'register':
                self.clean_input()

        except ValueError as e:
            widget: AlertWindow = AlertWindow(f"Erro: {str(e)}")
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
        self.silte_input.clear()
        self.sand_input.clear()
        self.clay_input.clear()

