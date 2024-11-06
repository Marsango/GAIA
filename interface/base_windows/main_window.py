# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.7.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QMainWindow, QMenu, QMenuBar, QSizePolicy,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1958, 1151)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.actionPropriedade = QAction(MainWindow)
        self.actionPropriedade.setObjectName(u"actionPropriedade")
        self.actionAmostra = QAction(MainWindow)
        self.actionAmostra.setObjectName(u"actionAmostra")
        self.actionGerar_laudo = QAction(MainWindow)
        self.actionGerar_laudo.setObjectName(u"actionGerar_laudo")
        self.actionConsultar_laudo = QAction(MainWindow)
        self.actionConsultar_laudo.setObjectName(u"actionConsultar_laudo")
        self.actionGr_ficos = QAction(MainWindow)
        self.actionGr_ficos.setObjectName(u"actionGr_ficos")
        self.actionFatores_vari_veis = QAction(MainWindow)
        self.actionFatores_vari_veis.setObjectName(u"actionFatores_vari_veis")
        self.actionPessoa_F_sica = QAction(MainWindow)
        self.actionPessoa_F_sica.setObjectName(u"actionPessoa_F_sica")
        self.actionPessoa_Jur_dica = QAction(MainWindow)
        self.actionPessoa_Jur_dica.setObjectName(u"actionPessoa_Jur_dica")
        self.actionSolicitantes = QAction(MainWindow)
        self.actionSolicitantes.setObjectName(u"actionSolicitantes")
        self.actionSobre = QAction(MainWindow)
        self.actionSobre.setObjectName(u"actionSobre")
        self.actionConsultar_laudo_2 = QAction(MainWindow)
        self.actionConsultar_laudo_2.setObjectName(u"actionConsultar_laudo_2")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setEnabled(True)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setStyleSheet(u"color: rgb(70, 0, 0);")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, -1, 0)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setPixmap(QPixmap(u"../../../../Downloads/UpscaleImage_1_20240722.jpeg"))
        self.label.setScaledContents(False)
        self.label.setTextInteractionFlags(Qt.NoTextInteraction)

        self.horizontalLayout.addWidget(self.label)


        self.horizontalLayout_2.addWidget(self.frame)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1958, 21))
        self.menuCadastro = QMenu(self.menubar)
        self.menuCadastro.setObjectName(u"menuCadastro")
        self.menuConfigura_es = QMenu(self.menubar)
        self.menuConfigura_es.setObjectName(u"menuConfigura_es")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuCadastro.menuAction())
        self.menubar.addAction(self.menuConfigura_es.menuAction())
        self.menuCadastro.addAction(self.actionSolicitantes)
        self.menuCadastro.addAction(self.actionConsultar_laudo_2)
        self.menuConfigura_es.addAction(self.actionFatores_vari_veis)
        self.menuConfigura_es.addAction(self.actionSobre)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionPropriedade.setText(QCoreApplication.translate("MainWindow", u"Propriedade", None))
        self.actionAmostra.setText(QCoreApplication.translate("MainWindow", u"Amostra", None))
        self.actionGerar_laudo.setText(QCoreApplication.translate("MainWindow", u"Gerar laudo", None))
        self.actionConsultar_laudo.setText(QCoreApplication.translate("MainWindow", u"Consultar laudo", None))
        self.actionGr_ficos.setText(QCoreApplication.translate("MainWindow", u"Graficos", None))
        self.actionFatores_vari_veis.setText(QCoreApplication.translate("MainWindow", u"Fatores variaveis", None))
        self.actionPessoa_F_sica.setText(QCoreApplication.translate("MainWindow", u"Pessoa F\u00edsica", None))
        self.actionPessoa_Jur_dica.setText(QCoreApplication.translate("MainWindow", u"Pessoa Jur\u00eddica", None))
        self.actionSolicitantes.setText(QCoreApplication.translate("MainWindow", u"Solicitantes", None))
        self.actionSobre.setText(QCoreApplication.translate("MainWindow", u"Sobre", None))
        self.actionConsultar_laudo_2.setText(QCoreApplication.translate("MainWindow", u"Consultar laudo", None))
        self.label.setText("")
        self.menuCadastro.setTitle(QCoreApplication.translate("MainWindow", u"Cadastro", None))
        self.menuConfigura_es.setTitle(QCoreApplication.translate("MainWindow", u"Configuracoes", None))
    # retranslateUi

