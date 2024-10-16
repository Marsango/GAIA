import sqlite3

from PySide6 import QtCore
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from backend.classes.GraphParameters import GraphParameters
from backend.classes.Database import Database
from interface.base_windows.generate_report import GenerateReportDialog
from PySide6.QtWidgets import (QDialog, QTableWidgetItem, QHeaderView, QFileDialog)


class GenerateReport(QDialog, GenerateReportDialog):
    def __init__(self, sample_id: int) -> None:
        super(GenerateReport, self).__init__()
        self.setupUi(self)
        self.sample_id = sample_id
        self.tableWidget.setRowCount(16)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        available_graphs: list[str] = ['Matéria Orgânica - MO', 'Fósforo - P', 'Potássio - K', 'Cobre - Cu', 'Ferro - Fe',
                            'Zinco - Zn', 'Manganês - Mn', 'pH CaCl', 'Índice SMP', 'Alumínio - Al', 'H + Al',
                            'Cálcio - Ca', 'Magnésio - Mg', 'Soma de Bases - SB', 'V (%)', ' Sat. Alumínio']
        for row, name in enumerate(available_graphs):
            check_box_item = QTableWidgetItem(name)
            check_box_item.setText(name)
            check_box_item.setFlags(QtCore.Qt.ItemFlag.ItemIsUserCheckable | QtCore.Qt.ItemFlag.ItemIsEnabled)
            check_box_item.setCheckState(QtCore.Qt.CheckState.Unchecked)
            self.tableWidget.setItem(row, 0, check_box_item)
        self.get_graph_values()
        self.select_all.clicked.connect(self.select_all_function)
        self.tableWidget.itemChanged.connect(self.update_graph_values)
        self.generate_report.clicked.connect(self.open_save_dialog)

    def select_all_function(self):
        for row in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(row, 0)
            item.setCheckState(QtCore.Qt.CheckState.Checked)

    def update_graph_values(self, item: QTableWidgetItem):
        if item.column() != 0:
            new_values: dict[str, float] = {'very low': float(self.tableWidget.item(item.row(), 1).text()),
                                            'low': float(self.tableWidget.item(item.row(), 2).text()),
                                            'medium': float(self.tableWidget.item(item.row(), 3).text()),
                                            'high': float(self.tableWidget.item(item.row(), 4).text()),
                                            'very high': float(self.tableWidget.item(item.row(), 5).text())}
            graph_parameters: GraphParameters = GraphParameters()
            graph_name: str = self.tableWidget.item(item.row(), 0).text()
            graph_parameters.set_graph_parameters(graph_name, new_values)

    def get_graph_values(self):
        graph_parameters: GraphParameters = GraphParameters()
        for row in range(self.tableWidget.rowCount()):
            current_row: str = self.tableWidget.item(row, 0).text()
            parameters: dict[str, float] = graph_parameters.get_graph_parameters(current_row)
            self.tableWidget.setItem(row, 1, QTableWidgetItem(str(parameters["very low"])))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(str(parameters["low"])))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(str(parameters["medium"])))
            self.tableWidget.setItem(row, 4, QTableWidgetItem(str(parameters["high"])))
            self.tableWidget.setItem(row, 5, QTableWidgetItem(str(parameters["very high"])))

    def open_save_dialog(self):
        filename: QFileDialog.getSaveFileName = QFileDialog.getSaveFileName()
        db: Database = Database()
        sample_info: sqlite3.Row = db.get_sample_info(self.sample_id)
        self.generate_pdf(filename[0], sample_info)

    def add_fonts(self):
        pdfmetrics.registerFont(TTFont('arial', 'fonts/arial.ttf'))
        pdfmetrics.registerFont(TTFont('arialbd', 'fonts/arialbd.ttf'))
        pdfmetrics.registerFont(TTFont('arialbi', 'fonts/arialbi.ttf'))
        pdfmetrics.registerFont(TTFont('ariali', 'fonts/ariali.ttf'))
        pdfmetrics.registerFont(TTFont('arilbk', 'fonts/ariblk.ttf'))

    def generate_pdf(self, path: str, sample_info: sqlite3.Row):
        self.add_fonts()
        pdf: canvas.Canvas = canvas.Canvas(f'{path}.pdf')
        pdf.setTitle('Laudo - 001')
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
        pdf.line(70, 720, 520, 720)
        pdf.line(70, 720, 70, 665)
        pdf.line(70, 665, 520, 665)
        pdf.line(520, 720, 520, 665)
        pdf.setFont('arial', 10)
        pdf.drawString(75, 710, f"Solicitante: {sample_info['requester_name']}")
        pdf.drawString(75, 700, f"Endereço: {sample_info['address']}")
        pdf.drawString(75, 690, f"Propriedade: {sample_info['property_name']}")
        pdf.drawString(75, 680, f"Talhão: {sample_info['sample_name']}")
        pdf.drawString(75, 670, f"Técnico: -/-")
        pdf.drawString(400, 710, f"Laudo: -/-")
        pdf.drawString(400, 700, f"Amostra: {sample_info['sample_number']}")
        pdf.drawString(400, 690, f"Data: {sample_info['collection_date']}")
        pdf.drawString(400, 680, f"Profundidade: {sample_info['depth']}")
        pdf.drawString(400, 670, f"Nº Matrícula: {sample_info['registration_number']}")
        pdf.save()