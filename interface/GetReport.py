import os
import shutil
from pathlib import Path

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (QDialog, QTableWidgetItem, QAbstractItemView, QHeaderView, QFileDialog)
from interface.AlertWindow import AlertWindow
from interface.base_windows.get_report import GetReportDialog
from backend.classes.Database import Database
import sqlite3

class GetReport(QDialog, GetReportDialog):
    def __init__(self) -> None:
        super(GetReport, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Laudos cadastrados')
        self.setWindowIcon(QPixmap(os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "interface",
            "images"
        ).replace("\\", "/") + "/GAIA_icon.png"))
        self.report_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.report_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.report_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.report_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.report_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.copy_button.clicked.connect(self.make_copy)
        self.refresh_table()

    def refresh_table(self) -> None:
        db: Database = Database()
        reports: list[sqlite3.Row] = db.get_report_info()
        self.report_table.setRowCount(0)
        for report in reports:
            row_position: int = self.report_table.rowCount()
            self.report_table.insertRow(row_position)
            self.report_table.setItem(row_position, 0, QTableWidgetItem(str(report['id'])))
            self.report_table.setItem(row_position, 1, QTableWidgetItem(str(report['requester_name'])))
            self.report_table.setItem(row_position, 2, QTableWidgetItem(str(report['date'])))
            self.report_table.setItem(row_position, 3, QTableWidgetItem(str(report['property'])))

    def make_copy(self) -> None:
        selected_items: list[QTableWidgetItem] = self.report_table.selectedIndexes()
        if len(selected_items) == 0:
            widget: AlertWindow = AlertWindow("Você deve selecionar um laudo para copiar.")
            widget.exec()
            return
        for data in selected_items:
            if data.row() != selected_items[0].row():
                widget: AlertWindow = AlertWindow("Você só pode copiar um laudo por vez.")
                widget.exec()
                return
        row: int = selected_items[0].row()
        id: int = int(self.report_table.item(row, 0).text())
        file_path = self.open_save_dialog()
        script_path: Path = Path(__file__).resolve()
        backup_path: Path = script_path.parent.parent / "reports" / f"Laudo - {id}.pdf"
        shutil.copy(backup_path, file_path)
        widget: AlertWindow = AlertWindow("Cópia feita com sucesso!")
        widget.exec()

    def open_save_dialog(self) -> str:
        filename: QFileDialog.getSaveFileName = QFileDialog.getSaveFileName(filter="*.pdf")
        return filename[0]