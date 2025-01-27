import json
import os

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (QDialog)

from backend.classes.Configuration import Configuration
from interface.base_windows.register_sample import RegisterSampleDialog
from backend.classes.Database import Database
from backend.classes.Sample import Sample
from interface.AlertWindow import AlertWindow


class RegisterSample(QDialog, RegisterSampleDialog):
    def __init__(self, property_id: int) -> None:
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
        self.sample_number.setText(str(sample_data["sample_number"]))
        self.collection_depth.setText(str(sample_data["depth"]))
        self.date.setText(sample_data["collection_date"])
        self.description.setText(sample_data["description"])
        self.area.setText(str(sample_data["total_area"]))
        self.latitude.setText(str(sample_data["latitude"]))
        self.longitude.setText(str(sample_data["longitude"]))
        used_config = json.loads(sample_data['used_config'])
        if sample_data["phosphorus"] is None:
            self.phosphorus.setText('')
        else:
            if used_config['phosphorus']['selected'] == 'factors':
                self.phosphorus.setText(str(round(sample_data["phosphorus"]/used_config['phosphorus']['value'], 2)))
            else:
                self.phosphorus.setText(str(round(
                    sample_data["phosphorus"]*used_config['phosphorus']['value']['a']
                    + used_config['phosphorus']['value']['b'], 2)))

        if sample_data["potassium"] is None:
            self.potassium.setText('')
        else:
            if used_config['phosphorus']['selected'] == 'factors':
                self.potassium.setText(str(round(sample_data["potassium"]/used_config['potassium']['value'], 2)))
            else:
                self.potassium.setText(str(round(
                    sample_data["potassium"]*used_config['potassium']['value']['a']
                    + used_config['potassium']['value']['b'], 2)))

        if sample_data["organic_matter"] is None:
            self.organic_matter.setText('')
        else:
            if used_config['organic_matter']['selected'] == 'factors':
                self.organic_matter.setText(str(round(sample_data["potassium"]/used_config['potassium']['value'], 2)))
            else:
                self.organic_matter.setText(str(round(
                    sample_data["organic_matter"]*used_config['potassium']['value']['a']
                    + used_config['organic_matter']['value']['b'], 2)))

        self.clay_input.setText(str(sample_data["clay"]) if sample_data["clay"] is not None else '')
        self.silte_input.setText(str(sample_data["silte"]) if sample_data["silte"] is not None else '')
        self.sand_input.setText(str(sample_data["sand"]) if sample_data["sand"] is not None else '')
        self.ph.setText(str(sample_data["ph"]) if sample_data["ph"] is not None else '')
        self.SMP.setText(str(sample_data["smp"]) if sample_data["smp"] is not None else '')
        self.read_aluminum.setText(str(sample_data["aluminum"]) if sample_data["aluminum"] is not None else '')
        self.read_calcium.setText(str(sample_data["calcium"]) if sample_data["calcium"] is not None else '')
        self.read_magnesium.setText(str(sample_data["magnesium"]) if sample_data["magnesium"] is not None else '')
        self.read_copper.setText(str(sample_data["copper"]) if sample_data["copper"] is not None else '')
        self.read_iron.setText(str(sample_data["iron"]) if sample_data["iron"] is not None else '')
        self.read_manganese.setText(str(sample_data["manganese"]) if sample_data["manganese"] is not None else '')
        self.read_zinc.setText(str(sample_data["zinc"]) if sample_data["zinc"] is not None else '')
        self.blank_test_aluminum.setText('0')
        self.blank_test_calcium.setText('0')
        self.blank_test_magnesium.setText('0')
        self.blank_test_copper.setText('0')
        self.blank_test_iron.setText('0')
        self.blank_test_manganese.setText('0')
        self.blank_test_zinc.setText('0')
        self.register_button.setText("Salvar alterações")
        self.setWindowTitle('Edição de registro de amostra')
        self.mode = 'edit'
        self.current_sample_id = int(sample_data['id'])

    def register_action(self) -> None:
        db: Database = Database()
        try:
            if not self.collection_depth.text() or not self.area.text() or not self.latitude.text() or not self.longitude.text() or not self.sample_number.text():
                raise ValueError("Por favor, preencha todos os campos obrigatórios.")
            depth: float = float(self.collection_depth.text())
            total_area: float = float(self.area.text())
            latitude: float = float(self.latitude.text())
            longitude: float = float(self.longitude.text())
            sand: float | None = float(self.sand_input.text()) if self.sand_input.text() != '' else None
            silte: float | None = float(self.silte_input.text()) if self.silte_input.text() != '' else None
            clay: float | None = float(self.clay_input.text()) if self.clay_input.text() != '' else None
            phosphorus: float | None = float(self.phosphorus.text()) if self.phosphorus.text() != '' else None
            potassium: float | None = float(self.potassium.text()) if self.potassium.text() != '' else None
            organic_matter: float | None = float(self.organic_matter.text()) if self.organic_matter.text() != '' else None
            ph: float | None = float(self.ph.text()) if self.ph.text() != '' else None
            smp: float | None = float(self.SMP.text()) if self.SMP.text() != '' else None
            blank_aluminum: float = float(self.blank_test_aluminum.text()) if self.blank_test_aluminum.text() != '' else 0.0
            aluminum: float | None = (float(self.read_aluminum.text()) - blank_aluminum) if self.read_aluminum.text() != '' else None
            blank_calcium: float = float(self.blank_test_calcium.text()) if self.blank_test_calcium.text() != '' else 0.0
            calcium: float | None = (float(self.read_calcium.text()) - blank_calcium) if self.read_calcium.text() != '' else None
            blank_magnesium: float = float(self.blank_test_magnesium.text()) if self.blank_test_magnesium.text() != '' else 0.0
            magnesium: float | None = (float(self.read_magnesium.text()) - blank_magnesium) if self.read_magnesium.text() != '' else None
            blank_copper: float = float(self.blank_test_copper.text()) if self.blank_test_copper.text() != '' else 0.0
            copper: float | None = (float(self.read_copper.text()) - blank_copper) if self.read_copper.text() != '' else None
            blank_iron: float = float(self.blank_test_iron.text()) if self.blank_test_iron.text() != '' else 0.0
            iron: float | None = (float(self.read_iron.text()) - blank_iron) if self.read_iron.text() != '' else None
            blank_manganese: float = float(self.blank_test_manganese.text()) if self.blank_test_manganese.text() != '' else 0.0
            manganese: float | None = (float(self.read_manganese.text()) - blank_manganese) if self.read_manganese.text() != '' else None
            blank_zinc: float = float(self.blank_test_zinc.text()) if self.blank_test_zinc.text() != '' else 0.0
            zinc: float | None = (float(self.read_zinc.text()) - blank_zinc) if self.read_zinc.text() != '' else None
            if sand is not None or silte is not None or clay is not None:
                if float(silte) + float(clay) + float(sand) != 100:
                    raise ValueError("A soma dos valores granulométricos deve ser igual a 100%.")
            if self.mode == 'register':
                is_editing = False
            else:
                is_editing = True
            sample: Sample = Sample(depth=depth, collection_date=self.date.text(),
                                    description=self.description.text(), total_area=total_area,
                                    latitude=latitude, longitude=longitude,
                                    phosphorus=phosphorus, potassium=potassium,
                                    organic_matter=organic_matter, ph=ph, smp=smp,
                                    aluminum=aluminum,
                                    calcium=calcium,
                                    magnesium=magnesium,
                                    copper=copper,
                                    iron=iron,
                                    manganese=manganese,
                                    zinc=zinc, clay=clay, sand=sand, silte=silte, is_editing=is_editing, sample_id = self.current_sample_id)
            if self.mode == 'register':
                db.insert_sample(sample, self.current_property_id, int(self.sample_number.text()))
                success: str = "Amostra registrada com sucesso!"
            else:
                db.edit_sample(sample, self.current_sample_id)
                success: str = "Alterações salvas com sucesso!"

            widget: AlertWindow = AlertWindow(success)
            widget.exec()

            if self.mode == 'register':
                self.clean_input()
        except ValueError as e:
            widget: AlertWindow = AlertWindow(f"Erro: {str(e)}")
            widget.exec()
        except TypeError as e:
            widget: AlertWindow = AlertWindow(f"Erro: você deve preencher o restante dos valores granulométricos.")
            widget.exec()
        db.close_connection()


    def clean_input(self):
        self.sample_number.clear()
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