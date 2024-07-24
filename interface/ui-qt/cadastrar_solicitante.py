# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'cadastrar_solicitante.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGroupBox, QHBoxLayout,
    QLineEdit, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(600, 350)
        Form.setMinimumSize(QSize(600, 350))
        Form.setMaximumSize(QSize(600, 350))
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.top_frame = QFrame(Form)
        self.top_frame.setObjectName(u"top_frame")
        self.top_frame.setAutoFillBackground(False)
        self.top_frame.setStyleSheet(u"QFrame#top_frame { \n"
" border: none; background: transparent;\n"
" }")
        self.top_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.top_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.top_frame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.left_frame = QFrame(self.top_frame)
        self.left_frame.setObjectName(u"left_frame")
        self.left_frame.setStyleSheet(u"QFrame{\n"
"border: none; background: transparent;\n"
"}")
        self.left_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.left_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.left_frame)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.personal_data_gbox = QGroupBox(self.left_frame)
        self.personal_data_gbox.setObjectName(u"personal_data_gbox")
        self.personal_data_gbox.setMinimumSize(QSize(0, 175))
        self.personal_data_gbox.setMaximumSize(QSize(16777215, 200))
        self.personal_data_gbox.setAutoFillBackground(False)
        self.personal_data_gbox.setStyleSheet(u"")
        self.verticalLayout_2 = QVBoxLayout(self.personal_data_gbox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame = QFrame(self.personal_data_gbox)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.frame)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.lineEdit = QLineEdit(self.frame)
        self.lineEdit.setObjectName(u"lineEdit")

        self.verticalLayout_7.addWidget(self.lineEdit)

        self.lineEdit_5 = QLineEdit(self.frame)
        self.lineEdit_5.setObjectName(u"lineEdit_5")

        self.verticalLayout_7.addWidget(self.lineEdit_5)


        self.verticalLayout_2.addWidget(self.frame)

        self.frame_2 = QFrame(self.personal_data_gbox)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.groupBox = QGroupBox(self.frame_2)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMinimumSize(QSize(120, 30))
        self.groupBox.setMaximumSize(QSize(120, 50))
        self.verticalLayout_4 = QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.lineEdit_2 = QLineEdit(self.groupBox)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setMinimumSize(QSize(100, 15))
        self.lineEdit_2.setMaximumSize(QSize(100, 15))
        self.lineEdit_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_4.addWidget(self.lineEdit_2)


        self.horizontalLayout_3.addWidget(self.groupBox)

        self.groupBox_3 = QGroupBox(self.frame_2)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setMaximumSize(QSize(100, 50))
        self.horizontalLayout_5 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.lineEdit_3 = QLineEdit(self.groupBox_3)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setMinimumSize(QSize(80, 15))
        self.lineEdit_3.setMaximumSize(QSize(80, 15))
        self.lineEdit_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_3.setPlaceholderText(u"")

        self.horizontalLayout_5.addWidget(self.lineEdit_3)


        self.horizontalLayout_3.addWidget(self.groupBox_3)

        self.groupBox_2 = QGroupBox(self.frame_2)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setMaximumSize(QSize(125, 50))
        self.verticalLayout_6 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.lineEdit_4 = QLineEdit(self.groupBox_2)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_6.addWidget(self.lineEdit_4)


        self.horizontalLayout_3.addWidget(self.groupBox_2)


        self.verticalLayout_2.addWidget(self.frame_2)


        self.verticalLayout_5.addWidget(self.personal_data_gbox)

        self.frame_4 = QFrame(self.left_frame)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMaximumSize(QSize(16777215, 100))
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_4)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.register_button = QPushButton(self.frame_4)
        self.register_button.setObjectName(u"register_button")
        self.register_button.setMinimumSize(QSize(125, 25))
        self.register_button.setMaximumSize(QSize(125, 50))

        self.horizontalLayout.addWidget(self.register_button)


        self.verticalLayout_5.addWidget(self.frame_4)


        self.horizontalLayout_2.addWidget(self.left_frame)

        self.address_gbox = QGroupBox(self.top_frame)
        self.address_gbox.setObjectName(u"address_gbox")
        self.address_gbox.setMaximumSize(QSize(200, 16777215))
        self.verticalLayout_3 = QVBoxLayout(self.address_gbox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.lineEdit_6 = QLineEdit(self.address_gbox)
        self.lineEdit_6.setObjectName(u"lineEdit_6")

        self.verticalLayout_3.addWidget(self.lineEdit_6)

        self.lineEdit_7 = QLineEdit(self.address_gbox)
        self.lineEdit_7.setObjectName(u"lineEdit_7")

        self.verticalLayout_3.addWidget(self.lineEdit_7)

        self.lineEdit_8 = QLineEdit(self.address_gbox)
        self.lineEdit_8.setObjectName(u"lineEdit_8")

        self.verticalLayout_3.addWidget(self.lineEdit_8)

        self.lineEdit_9 = QLineEdit(self.address_gbox)
        self.lineEdit_9.setObjectName(u"lineEdit_9")

        self.verticalLayout_3.addWidget(self.lineEdit_9)

        self.lineEdit_10 = QLineEdit(self.address_gbox)
        self.lineEdit_10.setObjectName(u"lineEdit_10")

        self.verticalLayout_3.addWidget(self.lineEdit_10)

        self.lineEdit_11 = QLineEdit(self.address_gbox)
        self.lineEdit_11.setObjectName(u"lineEdit_11")

        self.verticalLayout_3.addWidget(self.lineEdit_11)


        self.horizontalLayout_2.addWidget(self.address_gbox)


        self.verticalLayout.addWidget(self.top_frame)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.personal_data_gbox.setTitle(QCoreApplication.translate("Form", u"Dados Pessoais", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("Form", u"Nome", None))
        self.lineEdit_5.setPlaceholderText(QCoreApplication.translate("Form", u"E-mail", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"CPF", None))
        self.lineEdit_2.setInputMask(QCoreApplication.translate("Form", u"999.999.999-99", None))
        self.lineEdit_2.setPlaceholderText("")
        self.groupBox_3.setTitle(QCoreApplication.translate("Form", u"Nascimento", None))
        self.lineEdit_3.setInputMask(QCoreApplication.translate("Form", u"99/99/9999", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"Telefone", None))
        self.lineEdit_4.setInputMask(QCoreApplication.translate("Form", u"(99)99999-9999", None))
        self.lineEdit_4.setPlaceholderText(QCoreApplication.translate("Form", u"Telefone", None))
        self.register_button.setText(QCoreApplication.translate("Form", u"Cadastrar Solicitante", None))
        self.address_gbox.setTitle(QCoreApplication.translate("Form", u"Endere\u00e7o", None))
        self.lineEdit_6.setPlaceholderText(QCoreApplication.translate("Form", u"Pa\u00eds", None))
        self.lineEdit_7.setPlaceholderText(QCoreApplication.translate("Form", u"Estado", None))
        self.lineEdit_8.setPlaceholderText(QCoreApplication.translate("Form", u"Cidade", None))
        self.lineEdit_9.setPlaceholderText(QCoreApplication.translate("Form", u"Rua", None))
        self.lineEdit_10.setText("")
        self.lineEdit_10.setPlaceholderText(QCoreApplication.translate("Form", u"N\u00famero", None))
        self.lineEdit_11.setPlaceholderText(QCoreApplication.translate("Form", u"CEP", None))
    # retranslateUi

