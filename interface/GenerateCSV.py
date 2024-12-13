import sqlite3

from PySide6 import QtCore, QtGui
import csv
from interface.base_windows.generate_csv import GenerateCSVDialog
from interface.AlertWindow import AlertWindow
from backend.classes.Database import Database
from PySide6.QtWidgets import (QDialog, QFileDialog, QTableWidgetItem, QHeaderView, QAbstractItemView)



class GenerateCSV(QDialog, GenerateCSVDialog):
    def __init__(self, selected_ids: list[int]) -> None:
        super(GenerateCSV, self).__init__()
        self.setupUi(self)
        self.selected_ids = selected_ids
        self.file_path.setReadOnly(True)
        self.path_button.clicked.connect(self.open_dialog)
        self.save_button.clicked.connect(self.save)
        self.select_all_button.clicked.connect(self.select_all_function)
        available_parameters: list[str] = ['Fósforo - P', 'Potássio - K', 'Cobre - Cu', 'Matéria Orgânica - MO',
                                       'Ferro - Fe',
                                       'Zinco - Zn', 'Manganês - Mn', 'pH CaCl', 'Índice SMP', 'Alumínio - Al',
                                       'H + Al',
                                       'Cálcio - Ca', 'Magnésio - Mg', 'Soma de Bases - SB', 'V (%)', 'Sat. Alumínio']
        self.tableWidget.setRowCount(len(available_parameters) + 1)
        self.tableWidget.setColumnCount(1)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        first_item: QTableWidgetItem = QTableWidgetItem('Parâmetros')
        first_item.setTextAlignment(QtCore.Qt.AlignCenter)
        first_item.setBackground(QtGui.QColor(125,125,125))
        self.tableWidget.setItem(0, 0, first_item)
        for row, name in enumerate(available_parameters):
            check_box_item: QTableWidgetItem = QTableWidgetItem(name)
            check_box_item.setText(name)
            check_box_item.setFlags(QtCore.Qt.ItemFlag.ItemIsUserCheckable | QtCore.Qt.ItemFlag.ItemIsEnabled)
            check_box_item.setCheckState(QtCore.Qt.CheckState.Unchecked)
            self.tableWidget.setItem(row + 1, 0, check_box_item)

    def select_all_function(self) -> None:
        for row in range(1, self.tableWidget.rowCount()):
            item: QTableWidgetItem = self.tableWidget.item(row, 0)
            item.setCheckState(QtCore.Qt.CheckState.Checked)

    def open_dialog(self) -> None:
        filename: QFileDialog.getOpenFileName = QFileDialog.getSaveFileName()[0]
        self.file_path.setText(filename)

    def translate_params(self, params) -> str:
        translate_dict = {
            'Data': 'collection_date',
            'Descrição': 'description',
            'Número': 'sample_number',
            'Matéria Orgânica - MO': 'organic_matter',
            'Fósforo - P': 'phosphorus',
            'Potássio - K': 'potassium',
            'Cobre - Cu': 'copper',
            'Ferro - Fe': 'iron',
            'Zinco - Zn': 'zinc',
            'Manganês - Mn': 'manganese',
            'pH CaCl': 'ph',
            'Índice SMP': 'smp',
            'Alumínio - Al': 'aluminum',
            'H + Al': 'h_al',
            'Cálcio - Ca': 'calcium',
            'Magnésio - Mg': 'magnesium',
            'Soma de Bases - SB': 'base_sum',
            'V (%)': 'v_percent',
            'Sat. Alumínio': 'aluminum_saturation'
        }
        return translate_dict[params]

    def get_selected_parameters(self) -> list[str]:
        selected_parameters: list[str] = ['Data', 'Descrição', 'Número'] + [self.tableWidget.item(row, 0).text() for row in
                                          range(1, self.tableWidget.rowCount())
                                          if self.tableWidget.item(row, 0).checkState() == QtCore.Qt.CheckState.Checked]
        return selected_parameters

    def save(self) -> None:
        with open(f'{self.file_path.text()}.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            columns = self.get_selected_parameters()
            writer.writerow(columns)
            db: Database() = Database()
            not_numeric_columns: list[str] = ['Data', 'Descrição', 'Número']
            samples_info: list[sqlite3.Row] = db.get_samples(id_list = self.selected_ids)
            for sample_info in samples_info:
                sample_row: list[str] = []
                for parameter in columns:
                    if parameter not in not_numeric_columns: #and numbers_with_comma == True
                        sample_row.append(str(sample_info[self.translate_params(parameter)]).replace('.', ','))
                    else:
                        sample_row.append(sample_info[self.translate_params(parameter)])
                writer.writerow(sample_row)
        dialog: AlertWindow = AlertWindow("Arquivo salvo com sucesso!")
        dialog.exec()