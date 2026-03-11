import os

from interface.icon_utils import get_window_icon

from interface.base_windows.alert_window import AlertDialog
from PySide6.QtWidgets import (QDialog)


class AlertWindow(QDialog, AlertDialog):
    def __init__(self, message) -> None:
        super(AlertWindow, self).__init__()  # Inicializa a classe base
        self.setupUi(self)  # Configura a interface da janela com base no design do AlertDialog
        self.setWindowTitle('Alerta!')  # Define o título da janela

        # Define o ícone da janela com o caminho absoluto da imagem
        self.setWindowIcon(get_window_icon())

        self.label_2.setText(message)  # Define o texto da mensagem no label_2
        self.pushButton.clicked.connect(self.close)  # Conecta o botão para fechar a janela ao ser clicado