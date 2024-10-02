# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'register_property.ui'
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

class RegisterPropertyDialog(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(650, 278)
        Form.setMinimumSize(QSize(650, 200))
        Form.setMaximumSize(QSize(650, 278))
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.top_frame = QFrame(Form)
        self.top_frame.setObjectName(u"top_frame")
        self.top_frame.setAutoFillBackground(False)
        self.top_frame.setStyleSheet(u"QFrame#top_frame { \n"
" border: none; background: transparent;\n"
" }")
        self.top_frame.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_2 = QHBoxLayout(self.top_frame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.left_frame = QFrame(self.top_frame)
        self.left_frame.setObjectName(u"left_frame")
        self.left_frame.setStyleSheet(u"QFrame{\n"
"border: none; background: transparent;\n"
"}")
        self.left_frame.setFrameShape(QFrame.NoFrame)
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
        self.frame.setFrameShape(QFrame.NoFrame)
        self.verticalLayout_7 = QVBoxLayout(self.frame)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.name_input = QLineEdit(self.frame)
        self.name_input.setObjectName(u"name_input")

        self.verticalLayout_7.addWidget(self.name_input)

        self.registration_number_input = QLineEdit(self.frame)
        self.registration_number_input.setObjectName(u"registration_number_input")

        self.verticalLayout_7.addWidget(self.registration_number_input)


        self.verticalLayout_2.addWidget(self.frame)


        self.verticalLayout_5.addWidget(self.personal_data_gbox)

        self.frame_4 = QFrame(self.left_frame)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMaximumSize(QSize(16777215, 100))
        self.frame_4.setFrameShape(QFrame.NoFrame)
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

        self.location_input = QLineEdit(self.address_gbox)
        self.location_input.setObjectName(u"location_input")

        self.verticalLayout_3.addWidget(self.location_input)


        self.horizontalLayout_2.addWidget(self.address_gbox)


        self.verticalLayout.addWidget(self.top_frame)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.personal_data_gbox.setTitle(QCoreApplication.translate("Form", u"Dados da propriedade", None))
        self.name_input.setPlaceholderText(QCoreApplication.translate("Form", u"Nome", None))
        self.registration_number_input.setPlaceholderText(QCoreApplication.translate("Form", u"N\u00ba de matr\u00edcula", None))
        self.register_button.setText(QCoreApplication.translate("Form", u"Cadastrar Propriedade", None))
        self.address_gbox.setTitle(QCoreApplication.translate("Form", u"Endere\u00e7o", None))
        self.country_input.setPlaceholderText(QCoreApplication.translate("Form", u"Pa\u00eds", None))
        self.state_input.setPlaceholderText(QCoreApplication.translate("Form", u"Estado", None))
        self.city_input.setPlaceholderText(QCoreApplication.translate("Form", u"Cidade", None))
        self.location_input.setText("")
        self.location_input.setPlaceholderText(QCoreApplication.translate("Form", u"Localiza\u00e7\u00e3o", None))
    # retranslateUi

