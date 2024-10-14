
from PySide6 import QtCore

from backend.classes.GraphParameters import GraphParameters
from interface.base_windows.generate_report import GenerateReportDialog
from PySide6.QtWidgets import (QDialog, QTableWidgetItem, QHeaderView)


class GenerateReport(QDialog, GenerateReportDialog):
    def __init__(self) -> None:
        super(GenerateReport, self).__init__()
        self.setupUi(self)
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


