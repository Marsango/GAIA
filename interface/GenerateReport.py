import sqlite3
from itertools import pairwise
from pathlib import Path
from typing import Any
import matplotlib.pyplot as plt
import numpy as np
from PySide6 import QtCore
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from backend.classes.GraphParameters import GraphParameters
from backend.classes.Database import Database
from interface.base_windows.generate_report import GenerateReportDialog
from interface.AlertWindow import AlertWindow
from backend.classes.utils import handle_exception
from backend.classes.Report import Report
from PySide6.QtWidgets import (QDialog, QTableWidgetItem, QHeaderView, QFileDialog)
import shutil


class GenerateReport(QDialog, GenerateReportDialog):
    def __init__(self, sample_id: int) -> None:
        super(GenerateReport, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Gerar Relatório')
        self.sample_id = sample_id
        self.parameters_table.setRowCount(16)
        self.parameters_table.verticalHeader().setVisible(False)
        self.parameters_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.parameters_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        available_graphs: list[str] = ['Fósforo - P', 'Potássio - K', 'Cobre - Cu', 'Matéria Orgânica - MO',
                                       'Ferro - Fe',
                                       'Zinco - Zn', 'Manganês - Mn', 'pH CaCl', 'Índice SMP', 'Alumínio - Al',
                                       'H + Al',
                                       'Cálcio - Ca', 'Magnésio - Mg', 'Soma de Bases - SB', 'V (%)', ' Sat. Alumínio']
        for row, name in enumerate(available_graphs):
            check_box_item = QTableWidgetItem(name)
            check_box_item.setText(name)
            check_box_item.setFlags(QtCore.Qt.ItemFlag.ItemIsUserCheckable | QtCore.Qt.ItemFlag.ItemIsEnabled)
            check_box_item.setCheckState(QtCore.Qt.CheckState.Unchecked)
            self.parameters_table.setItem(row, 0, check_box_item)
        self.get_graph_values()
        self.select_all.clicked.connect(self.select_all_function)
        self.parameters_table.itemChanged.connect(self.update_graph_values)
        self.generate_report.clicked.connect(self.create_report)

    def select_all_function(self) -> None:
        for row in range(self.parameters_table.rowCount()):
            item = self.parameters_table.item(row, 0)
            item.setCheckState(QtCore.Qt.CheckState.Checked)

    def update_graph_values(self, item: QTableWidgetItem) -> None:
        if item.column() != 0:
            try:
                new_values: dict[str, float] = {'very low': float(self.parameters_table.item(item.row(), 1).text()),
                                                'low': float(self.parameters_table.item(item.row(), 2).text()),
                                                'medium': float(self.parameters_table.item(item.row(), 3).text()),
                                                'high': float(self.parameters_table.item(item.row(), 4).text()),
                                                'very high': float(self.parameters_table.item(item.row(), 5).text())}
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
        try:
            if self.technician_input.text() == '':
                raise ValueError("Error with values of 'técnico'")
            file_path = self.open_save_dialog()
            sample_info: sqlite3.Row = db.get_sample_info(self.sample_id)
            current_sample: sqlite3.Row = db.get_samples(sample_id=self.sample_id)[0]
            selected_parameters: dict[str, dict[str, float]] = self.get_selected_parameters()
            v_percent_intervals: dict[str, float] = selected_parameters.pop('V (%)')
            aluminum_intervals: dict[str, float] = selected_parameters.pop(' Sat. Alumínio')
            report_id: int  = db.get_next_report_id()
            self.plot_bar_graphs(selected_parameters, current_sample)
            self.plot_v_percent(current_sample['v_percent'], current_sample['ctc'], v_percent_intervals)
            self.plot_aluminum(current_sample['aluminum_saturation'], current_sample['base_sum'], aluminum_intervals)
            self.plot_ctc_graph(current_sample['potassium'], current_sample['magnesium'],
                                current_sample['calcium'], current_sample['h_al'])
            self.generate_pdf(file_path, sample_info, report_id)
            script_path: Path = Path(__file__).resolve()
            backup_path: Path = script_path.parent.parent / "reports" / f"Laudo - {report_id}.pdf"
            shutil.copy(file_path, backup_path)
            report: Report = Report(file_location=str(backup_path), technician=self.technician_input.text())
            db.insert_report(report, self.sample_id)

        except Exception as e:
            error = handle_exception(e)
            widget: AlertWindow = AlertWindow(error)
            widget.exec()
        finally:
            db.close_connection()

    def open_save_dialog(self) -> str:
        filename: QFileDialog.getSaveFileName = QFileDialog.getSaveFileName(filter="*.pdf")
        return filename[0]

    def add_fonts(self) -> None:
        pdfmetrics.registerFont(TTFont('arial', 'fonts/arial.ttf'))
        pdfmetrics.registerFont(TTFont('arialbd', 'fonts/arialbd.ttf'))
        pdfmetrics.registerFont(TTFont('arialbi', 'fonts/arialbi.ttf'))
        pdfmetrics.registerFont(TTFont('ariali', 'fonts/ariali.ttf'))
        pdfmetrics.registerFont(TTFont('arilbk', 'fonts/ariblk.ttf'))

    def setup_pdf(self, path: str, report_id: int) -> canvas.Canvas:
        self.add_fonts()
        pdf: canvas.Canvas = canvas.Canvas(f'{path}')
        pdf.setTitle(f'Laudo - {report_id}')
        return pdf

    def draw_header(self, pdf: canvas.Canvas) -> None:
        pdf.line(30, 750, 560, 750)
        pdf.setFont('arialbd', 14)
        pdf.drawCentredString(300, 730, 'Laudo de Análise de Solo')
        pdf.drawImage('images/UTFPR_logo.svg.png', 65, 725, 100, 100, preserveAspectRatio=True, mask='auto')
        pdf.drawImage('images/iapar-logo.png', 350, 728, 100, 100, preserveAspectRatio=True, mask='auto')
        pdf.setFont('arial', 8)
        pdf.drawString(170, 785, 'Ministério da educação', )
        pdf.drawString(170, 775, 'Universidade Tecnólogica Federal do Paraná')
        pdf.drawString(170, 765, 'Campus Pato Branco')
        pdf.drawString(170, 755, 'Coordenação de Agronomia')
        pdf.drawString(420, 785, 'Governo do Estado do Paraná')
        pdf.drawString(420, 775, 'Secretaria de Agricultura e Abastecimento')
        pdf.drawString(420, 765, 'Instituto Agronômico do Paraná')

    def draw_square(self, pdf: canvas.Canvas, pos_horizontal1: int, pos_horizontal2: int, pos_vertical1: int, pos_vertical2: int) -> None:
        pdf.line(pos_horizontal1, pos_vertical1, pos_horizontal2, pos_vertical1)
        pdf.line(pos_horizontal1, pos_vertical1, pos_horizontal1, pos_vertical2)
        pdf.line(pos_horizontal1, pos_vertical2, pos_horizontal2, pos_vertical2)
        pdf.line(pos_horizontal2, pos_vertical1, pos_horizontal2, pos_vertical2)

    def write_main_info_square(self, pdf: canvas.Canvas, sample_info: sqlite3.Row, report_id: int) -> None:
        self.draw_square(pdf, 70, 520, 720, 665)
        pdf.setFont('arial', 10)
        pdf.drawString(75, 710, f"Solicitante: {sample_info['requester_name']}")
        pdf.drawString(75, 700, f"Endereço: {sample_info['address']}")
        pdf.drawString(75, 690, f"Propriedade: {sample_info['property_name']}")
        pdf.drawString(75, 680, f"Talhão: {sample_info['sample_name']}")
        pdf.drawString(75, 670, f"Técnico: {self.technician_input.text()}")
        pdf.drawString(400, 710, f"Laudo: {report_id}")
        pdf.drawString(400, 700, f"Amostra: {sample_info['sample_number']}")
        pdf.drawString(400, 690, f"Data: {sample_info['collection_date']}")
        pdf.drawString(400, 680, f"Profundidade: {sample_info['depth']} cm")
        pdf.drawString(400, 670, f"Nº Matrícula: {sample_info['registration_number']}")

    def draw_graphs(self, pdf) -> None:
        pdf.drawImage('images/auxgraph.png', 85, 275, 400, 500, preserveAspectRatio=True, mask='auto')
        pdf.drawImage('images/v_percent_graph.png', 75, 225, 200, 200, preserveAspectRatio=True, mask='auto')
        pdf.drawImage('images/aluminum_graph.png', 300, 225, 200, 200, preserveAspectRatio=True, mask='auto')
        pdf.drawImage('images/ctc_and_values.png', 200, 65, 200, 200, preserveAspectRatio=True, mask='auto')

    def draw_footer(self, pdf):
        self.draw_square(pdf, 70, 520, 75, 50)
        pdf.setFont('arial', 8)
        pdf.drawCentredString(300, 65,
                              f"Laboratório de Análise de Solos UTFPR/IAPAR, Via do conhecimento, KM 01, CEP 85503-390, Pato Branco - PR")
        pdf.drawCentredString(300, 55, f"Telefone/WhatsApp: (46) 3220-2539")

    def generate_pdf(self, path: str, sample_info: sqlite3.Row, report_id: int) -> None:
        pdf = self.setup_pdf(path, report_id)
        self.draw_header(pdf)
        self.write_main_info_square(pdf, sample_info, report_id)
        self.draw_graphs(pdf)
        self.draw_footer(pdf)
        pdf.save()

    def verify_consistency(self, selected_parameters: dict[str, dict[str, float]]) -> None:
        for parameter, values in selected_parameters.items():
            for (key_a, val_a), (key_b, val_b) in pairwise(values.items()):
                if val_a >= val_b:
                    raise ValueError(f"Error with values of '{parameter}'")

    def get_selected_parameters(self) -> dict[str, dict[str, float]]:
        selected_parameters: dict[str, dict[str, float]] = {}
        for row in range(self.parameters_table.rowCount()):
            if self.parameters_table.item(row, 0).checkState() == QtCore.Qt.CheckState.Checked or self.parameters_table.item(row, 0).text() == ' Sat. Alumínio'\
                    or self.parameters_table.item(row, 0).text() == 'V (%)':
                selected_parameters[self.parameters_table.item(row, 0).text()] = {
                    'very low': float(self.parameters_table.item(row, 1).text()),
                    'low': float(self.parameters_table.item(row, 2).text()),
                    'medium': float(self.parameters_table.item(row, 3).text()),
                    'high': float(self.parameters_table.item(row, 4).text()),
                    'very high': float(self.parameters_table.item(row, 5).text())}
        self.verify_consistency(selected_parameters)
        return selected_parameters

    def traducao_intervalo(self, intervalo) -> str:
        traducao = {
            "very low": "Muito Baixo",
            "low": "Baixo",
            "medium": "Médio",
            "high": "Alto",
            "very high": "Muito Alto"
        }
        return traducao[intervalo]

    def plot_bar_graphs(self, data: dict[str, dict[str, float]], sample_data: sqlite3.Row) -> None:
        colors = {
            "Muito Alto": "red",
            "Alto": "orange",
            "Médio": "yellow",
            "Baixo": "green",
            "Muito Baixo": "blue"
        }

        sizes = {
            "Muito Alto": 4,
            "Alto": 3,
            "Médio": 2,
            "Baixo": 1,
            "Muito Baixo": 0
        }

        def get_color_and_bar_size(value, intervals) -> dict[str, Any]:
            interval_keys = list(intervals.keys())
            interval_values = list(intervals.values())
            for i in range(len(interval_values) - 1):
                if interval_values[i] <= value < interval_values[i + 1]:
                    key = interval_keys[i]
                    return {
                        'color': colors[self.traducao_intervalo(key)],
                        'size': sizes[self.traducao_intervalo(key)]
                    }
            key = interval_keys[-1]
            return {
                'color': colors[self.traducao_intervalo(key)],
                'size': sizes[self.traducao_intervalo(key)]
            }

        def translate_params(params) -> str:
            translate_dict = {
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

        dont_plot_list: list[str] = ['V (%)']
        fig, ax = plt.subplots(figsize=(10, 6))
        bar_width: float = 0.4
        bar_positions: np.arrange = np.arange(len(data))
        x_label: list[str] = []
        for i, (param, intervals) in enumerate(data.items()):
            if param.strip() not in dont_plot_list:
                value = sample_data[translate_params(param.strip())]
                color, bar_size = get_color_and_bar_size(value, intervals).values()

                ax.bar(i, bar_size, color=color, width=bar_width, label=f"{param} ({value})")
                x_label.append(f'{round(value, 2)}\n{param}')
        handles: list[plt.Rectangle] = [plt.Rectangle((0, 0), 1, 1, color=colors[key]) for key in colors]
        labels: list[str] = [key for key in colors]
        ax.legend(handles, labels, title="Intervalos", loc='upper right', bbox_to_anchor=(1, 1))
        ax.set_xticks(bar_positions)
        ax.set_xticklabels(x_label, rotation=45, ha='right')
        ax.set_yticks(range(len(list(sizes.keys()))))
        ax.set_yticklabels(list(sizes.keys())[::-1])
        ax.set_title('Gráfico das amostras')
        plt.tight_layout()
        plt.savefig('images/auxgraph.png', bbox_inches='tight')
        plt.close()

    def get_graph_title(self, value, intervals) -> str:
        for key, val in intervals.items():
            if value <= val:
                return self.traducao_intervalo(key)
        return "Muito Alto"

    def plot_v_percent(self, v_percent: float, ctc: float, v_percent_intervals: dict[str, float]) -> None:
        labels: list[str] = ['V (%)', 'CTC']
        sizes: list[float] = [v_percent, ctc]
        fig, ax = plt.subplots()
        ax.pie(sizes, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        ax.legend(labels, loc='upper left')
        plt.title(f"Resultado: {self.get_graph_title(v_percent, v_percent_intervals)}", x=0.5, y=-0.05)
        plt.savefig('images/v_percent_graph.png', bbox_inches='tight')

    def plot_aluminum(self, aluminum_saturation: float, base_sum: float, aluminum_intervals: dict[str, float]) -> None:
        labels: list[str] = ['Saturação por alumínio (m)', 'Soma de bases']
        sizes: list[float] = [aluminum_saturation, base_sum]
        fig, ax = plt.subplots()
        ax.pie(sizes, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        ax.legend(labels, loc='upper left')
        plt.title(f"Resultado: {self.get_graph_title(aluminum_saturation, aluminum_intervals)}", x=0.5, y=-0.05)
        plt.savefig('images/aluminum_graph.png', bbox_inches='tight')

    def plot_ctc_graph(self, potassium: float, magnesium: float, calcium: float, h_plus_al: float) -> None:
        labels: list[str] = ['Potássio - K', 'Magnésio - Mg', 'Cálcio - Ca', 'H + Al']
        sizes: list[float] = [potassium, magnesium, calcium, h_plus_al]
        fig, ax = plt.subplots()
        ax.pie(sizes, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        ax.legend(labels, loc='upper left')
        plt.savefig('images/ctc_and_values.png', bbox_inches='tight')
