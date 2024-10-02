# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'register_person.ui'
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

class RegisterPersonDialog(object):
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
        self.name_input = QLineEdit(self.frame)
        self.name_input.setObjectName(u"name_input")

        self.verticalLayout_7.addWidget(self.name_input)

        self.email_input = QLineEdit(self.frame)
        self.email_input.setObjectName(u"email_input")

        self.verticalLayout_7.addWidget(self.email_input)


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
        self.cpf_input = QLineEdit(self.groupBox)
        self.cpf_input.setObjectName(u"cpf_input")
        self.cpf_input.setMinimumSize(QSize(100, 15))
        self.cpf_input.setMaximumSize(QSize(100, 15))
        self.cpf_input.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_4.addWidget(self.cpf_input)


        self.horizontalLayout_3.addWidget(self.groupBox)

        self.groupBox_3 = QGroupBox(self.frame_2)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setMaximumSize(QSize(100, 50))
        self.horizontalLayout_5 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.birth_date_input = QLineEdit(self.groupBox_3)
        self.birth_date_input.setObjectName(u"birth_date_input")
        self.birth_date_input.setMinimumSize(QSize(80, 15))
        self.birth_date_input.setMaximumSize(QSize(80, 15))
        self.birth_date_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.birth_date_input.setPlaceholderText(u"")

        self.horizontalLayout_5.addWidget(self.birth_date_input)


        self.horizontalLayout_3.addWidget(self.groupBox_3)

        self.groupBox_2 = QGroupBox(self.frame_2)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setMaximumSize(QSize(125, 50))
        self.verticalLayout_6 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.phone_number_input = QLineEdit(self.groupBox_2)
        self.phone_number_input.setObjectName(u"phone_number_input")
        self.phone_number_input.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_6.addWidget(self.phone_number_input)


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
        self.country_input = QLineEdit(self.address_gbox)
        self.country_input.setObjectName(u"country_input")

        self.verticalLayout_3.addWidget(self.country_input)

        self.state_input = QLineEdit(self.address_gbox)
        self.state_input.setObjectName(u"state_input")

        self.verticalLayout_3.addWidget(self.state_input)

        self.city_input = QLineEdit(self.address_gbox)
        self.city_input.setObjectName(u"city_input")

        self.verticalLayout_3.addWidget(self.city_input)

        self.street_input = QLineEdit(self.address_gbox)
        self.street_input.setObjectName(u"street_input")

        self.verticalLayout_3.addWidget(self.street_input)

        self.address_number_input = QLineEdit(self.address_gbox)
        self.address_number_input.setObjectName(u"address_number_input")

        self.verticalLayout_3.addWidget(self.address_number_input)

        self.cep_input = QLineEdit(self.address_gbox)
        self.cep_input.setObjectName(u"cep_input")

        self.verticalLayout_3.addWidget(self.cep_input)


        self.horizontalLayout_2.addWidget(self.address_gbox)


        self.verticalLayout.addWidget(self.top_frame)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.personal_data_gbox.setTitle(QCoreApplication.translate("Form", u"Dados Pessoais", None))
        self.name_input.setPlaceholderText(QCoreApplication.translate("Form", u"Nome", None))
        self.email_input.setPlaceholderText(QCoreApplication.translate("Form", u"E-mail", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"CPF", None))
        self.cpf_input.setInputMask(QCoreApplication.translate("Form", u"999.999.999-99", None))
        self.cpf_input.setPlaceholderText("")
        self.groupBox_3.setTitle(QCoreApplication.translate("Form", u"Nascimento", None))
        self.birth_date_input.setInputMask(QCoreApplication.translate("Form", u"99/99/9999", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"Telefone", None))
        self.phone_number_input.setInputMask(QCoreApplication.translate("Form", u"(99)99999-9999", None))
        self.phone_number_input.setPlaceholderText(QCoreApplication.translate("Form", u"Telefone", None))
        self.register_button.setText(QCoreApplication.translate("Form", u"Cadastrar Solicitante", None))
        self.address_gbox.setTitle(QCoreApplication.translate("Form", u"Endere\u00e7o", None))
        self.country_input.setPlaceholderText(QCoreApplication.translate("Form", u"Pa\u00eds", None))
        self.state_input.setPlaceholderText(QCoreApplication.translate("Form", u"Estado", None))
        self.city_input.setPlaceholderText(QCoreApplication.translate("Form", u"Cidade", None))
        self.street_input.setPlaceholderText(QCoreApplication.translate("Form", u"Rua", None))
        self.address_number_input.setText("")
        self.address_number_input.setPlaceholderText(QCoreApplication.translate("Form", u"N\u00famero", None))
        self.cep_input.setPlaceholderText(QCoreApplication.translate("Form", u"CEP", None))
    # retranslateUi

