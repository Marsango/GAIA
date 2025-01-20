import os
import sqlite3

from PySide6 import QtCore, QtGui

import backend.classes.Report as Report
import shutil
from itertools import pairwise
from pathlib import Path
from PySide6.QtGui import QPixmap, QColor
from backend.classes.GraphParameters import GraphParameters
from backend.classes.Database import Database
from interface.base_windows.generate_report import GenerateReportDialog
from interface.AlertWindow import AlertWindow
from backend.classes.utils import handle_exception
from backend.classes.Report import Report
from PySide6.QtWidgets import (QDialog, QTableWidgetItem, QHeaderView, QFileDialog)


class GenerateReport(QDialog, GenerateReportDialog):
    def __init__(self, sample_id: int) -> None:
        super(GenerateReport, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Gerar Relatório')
        self.setWindowIcon(QPixmap(os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "interface",
            "images"
        ).replace("\\", "/") + "/logo_lab.png"))
        self.sample_id = sample_id
        self.label.setText('Convênio: ')
        self.parameters_table.verticalHeader().setVisible(False)
        self.parameters_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.parameters_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        available_graphs: list[str] = ['Fósforo - P', 'Potássio - K', 'Cobre - Cu', 'Matéria Orgânica - MO',
                                       'Zinco - Zn', 'Manganês - Mn', 'pH CaCl', 'Índice SMP', 'Alumínio - Al',
                                       'Cálcio - Ca', 'Magnésio - Mg', 'Soma de Bases - SB', 'V (%)', 'Sat. Alumínio',
                                       "CTC Efetiva", "CTC Potencial",
        ]
        self.parameters_table.setRowCount(len(available_graphs))
        self.__element_sample_mapping = {
            'Fósforo - P': 'phosphorus',
            'Potássio - K': 'potassium',
            'Cobre - Cu': 'copper',
            'Matéria Orgânica - MO': 'organic_matter',
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
            'Sat. Alumínio': 'aluminum_saturation',
            "CTC Efetiva": 'effective_ctc',
            "CTC Potencial": "ctc"
        }

        for row, name in enumerate(available_graphs):
            check_box_item: QTableWidgetItem = QTableWidgetItem(name)
            check_box_item.setText(name)
            check_box_item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
            check_box_item.setTextAlignment(QtCore.Qt.AlignCenter)
            check_box_item.setBackground(QtGui.QColor(125, 125, 125))
            self.parameters_table.setItem(row, 0, check_box_item)
        self.get_graph_values()
        self.parameters_table.itemChanged.connect(self.update_graph_values)
        self.generate_report.clicked.connect(self.create_report)


    def update_graph_values(self, item: QTableWidgetItem) -> None:
        if item.column() != 0:
            try:
                new_values: dict[str, float] = {'very low': round(float(self.parameters_table.item(item.row(), 1).text()), 2),
                                                'low': round(float(self.parameters_table.item(item.row(), 2).text()), 2),
                                                'medium': round(float(self.parameters_table.item(item.row(), 3).text()), 2),
                                                'high': round(float(self.parameters_table.item(item.row(), 4).text()), 2),
                                                'very high': round(float(self.parameters_table.item(item.row(), 5).text()), 2)}
                graph_parameters: GraphParameters = GraphParameters()
                graph_name: str = self.parameters_table.item(item.row(), 0).text()
                graph_parameters.set_graph_parameters(graph_name, new_values)
            except Exception as e:
                error = handle_exception(e)
                widget: AlertWindow = AlertWindow(error)
                widget.exec()
                self.parameters_table.blockSignals(True)
                self.get_graph_values()
                self.parameters_table.blockSignals(False)

    def get_graph_values(self) -> None:
        graph_parameters: GraphParameters = GraphParameters()
        for row in range(self.parameters_table.rowCount()):
            current_row: str = self.parameters_table.item(row, 0).text()
            parameters: dict[str, float] = graph_parameters.get_graph_parameters(current_row)
            self.parameters_table.setItem(row, 1, QTableWidgetItem(str(parameters["very low"])))
            self.parameters_table.setItem(row, 2, QTableWidgetItem(str(parameters["low"])))
            self.parameters_table.setItem(row, 3, QTableWidgetItem(str(parameters["medium"])))
            self.parameters_table.setItem(row, 4, QTableWidgetItem(str(parameters["high"])))
            self.parameters_table.setItem(row, 5, QTableWidgetItem(str(parameters["very high"])))

    def create_report(self):
        db: Database = Database()
        if self.technician_input.text() == '':
            error_message = "Erro: O campo de convênio está vazio. Por favor, insira um convênio."
            widget: AlertWindow = AlertWindow(error_message)
            widget.exec()
            return
        file_path = self.open_save_dialog()
        sample_info: sqlite3.Row = db.get_sample_info(self.sample_id)
        sample_values: sqlite3.Row = db.get_samples(sample_id=self.sample_id)[0]
        reference: dict[str, dict[str, float]] = self.get_selected_parameters()
        report_id: int = db.get_next_report_id()
        script_path: Path = Path(__file__).resolve()
        backup_path: Path = script_path.parent.parent / "reports" / f"Laudo - {report_id}.pdf"
        report: Report = Report(file_location=str(backup_path), agreement=self.technician_input.text())
        report.generate_pdf(sample_info, file_path, report_id, sample_values, reference)
        shutil.copy(file_path, backup_path)
        db.insert_report(report, self.sample_id)
        db.close_connection()

    def open_save_dialog(self) -> str:
        filename: QFileDialog.getSaveFileName = QFileDialog.getSaveFileName(filter="*.pdf")
        return filename[0]

    def verify_consistency(self, selected_parameters: dict[str, dict[str, float]]) -> None:
        for parameter, values in selected_parameters.items():
            for (key_a, val_a), (key_b, val_b) in pairwise(values.items()):
                if val_a >= val_b:
                    error_message = f"Erro: o valor {key_a} não pode ser maior que o {key_b} em {parameter}."
                    widget: AlertWindow = AlertWindow(error_message)
                    widget.exec()
                    return


    def get_selected_parameters(self) -> dict[str, dict[str, float]]:
        db: Database = Database()
        sample_info: sqlite3.Row = db.get_samples(sample_id=self.sample_id)[0]
        selected_parameters: dict[str, dict[str, float]] = {}
        for row in range(self.parameters_table.rowCount()):
            if sample_info[self.__element_sample_mapping[self.parameters_table.item(row, 0).text()]] is not None:
                selected_parameters[self.__element_sample_mapping[self.parameters_table.item(row, 0).text()]] = {
                    'very low': float(self.parameters_table.item(row, 1).text()),
                    'low': float(self.parameters_table.item(row, 2).text()),
                    'medium': float(self.parameters_table.item(row, 3).text()),
                    'high': float(self.parameters_table.item(row, 4).text()),
                    'very high': float(self.parameters_table.item(row, 5).text())}
        self.verify_consistency(selected_parameters)
        return selected_parameters



