from PIL.ImageQt import QPixmap

from interface.base_windows.backup_window import BackupDialog
from interface.AlertWindow import AlertWindow
from backend.classes.Database import Database
from PySide6.QtWidgets import (QDialog, QFileDialog)
import shutil, os
import datetime


class BackupWindow(QDialog, BackupDialog):
    def __init__(self) -> None:
        super(BackupWindow, self).__init__()  # Inicializa a classe base
        self.setupUi(self)  # Configura a interface da janela com base no design do BackupDialog

        # Define o caminho para o banco de dados
        self.__db_location = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),  # Diretório raiz do projeto
            "backend",
            "classes"
        ).replace("\\", "/") + "/soil_analysis.db"

        # Define o caminho para o diretório de relatórios
        self.__report_location = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "reports"
        ).replace("\\", "/")

        self.setWindowTitle('Opções de backup')  # Define o título da janela

        # Define o ícone da janela com o caminho absoluto da imagem
        self.setWindowIcon(QPixmap(os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "interface",
            "images"
        ).replace("\\", "/") + "/logo_lab.png"))

        # Instancia a classe Database para manipulação do banco de dados
        db: Database = Database()

        # Atualiza as informações da interface com os dados do banco
        self.requester_count.setText(str(len(db.get_requesters())))  # Número de solicitantes
        self.property_count.setText(str(len(db.get_properties())))  # Número de propriedades
        self.sample_count.setText(str(len(db.get_samples())))  # Número de amostras

        # Conecta os botões às funções correspondentes
        self.select_folder.clicked.connect(self.open_dialog)  # Botão para selecionar pasta
        self.backup_button.clicked.connect(self.backup)  # Botão para realizar o backup

    def open_dialog(self) -> None:
        filename: QFileDialog.getOpenFileName = QFileDialog.getExistingDirectory()  # Seleção do diretório
        self.backup_path.setText(filename)  # Atualiza o campo de texto com o caminho selecionado

    def backup(self) -> None:
        # Copia o banco de dados para o diretório de backup com um nome que inclui a data/hora
        shutil.copy(
            self.__db_location, 
            f"{self.backup_path.text()}/backup_gaia_{str(datetime.datetime.now()).split('.')[0].replace(' ', '_').replace(':', '-')}.db"
        )

        # Se a opção estiver marcada, copia também os relatórios para o diretório de backup
        if self.backup_checkbox.isChecked():
            shutil.copytree(self.__report_location, self.backup_path.text(), dirs_exist_ok=True)

        # Exibe uma janela de alerta indicando que o backup foi concluído
        dialog: AlertWindow = AlertWindow("Backup salvo com sucesso!")
        dialog.exec()

