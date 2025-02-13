import os

from PySide6.QtGui import QPixmap

from interface.base_windows.alert_window import AlertDialog
from PySide6.QtWidgets import (QDialog)


class AlertWindow(QDialog, AlertDialog):
    def __init__(self, message) -> None:
        super(AlertWindow, self).__init__()  # Inicializa a classe base
        self.setupUi(self)  # Configura a interface da janela com base no design do AlertDialog
        self.setWindowTitle('Alerta!')  # Define o título da janela

        # Define o ícone da janela com o caminho absoluto da imagem
        self.setWindowIcon(QPixmap(os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),  # Caminho do diretório atual
            "interface",  # Pasta interface
            "images"  # Subpasta images
        ).replace("\\", "/") + "/GAIA_icon.png"))  # Substitui barras invertidas por barras normais no caminho

        self.label_2.setText(message)  # Define o texto da mensagem no label_2
        self.pushButton.clicked.connect(self.close)  # Conecta o botão para fechar a janela ao ser clicado