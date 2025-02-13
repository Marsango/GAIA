# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'configuration_window.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class ConfigurationDialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(642, 377)
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox_2 = QGroupBox(self.groupBox)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.frame_2 = QFrame(self.groupBox_2)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setEnabled(True)
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.phosphorus_combobox = QComboBox(self.frame_2)
        self.phosphorus_combobox.addItem("")
        self.phosphorus_combobox.addItem("")
        self.phosphorus_combobox.setObjectName(u"phosphorus_combobox")

        self.horizontalLayout_3.addWidget(self.phosphorus_combobox)

        self.phosphorus_widget_factor = QWidget(self.frame_2)
        self.phosphorus_widget_factor.setObjectName(u"phosphorus_widget_factor")
        self.horizontalLayout_8 = QHBoxLayout(self.phosphorus_widget_factor)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label = QLabel(self.phosphorus_widget_factor)
        self.label.setObjectName(u"label")

        self.horizontalLayout_8.addWidget(self.label)

        self.phosphorus_factor = QLineEdit(self.phosphorus_widget_factor)
        self.phosphorus_factor.setObjectName(u"phosphorus_factor")

        self.horizontalLayout_8.addWidget(self.phosphorus_factor)


        self.horizontalLayout_3.addWidget(self.phosphorus_widget_factor)

        self.phosphorus_widget_line = QWidget(self.frame_2)
        self.phosphorus_widget_line.setObjectName(u"phosphorus_widget_line")
        self.horizontalLayout_11 = QHBoxLayout(self.phosphorus_widget_line)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_4 = QLabel(self.phosphorus_widget_line)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_11.addWidget(self.label_4)

        self.phosphorus_a = QLineEdit(self.phosphorus_widget_line)
        self.phosphorus_a.setObjectName(u"phosphorus_a")

        self.horizontalLayout_11.addWidget(self.phosphorus_a)

        self.label_7 = QLabel(self.phosphorus_widget_line)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_11.addWidget(self.label_7)

        self.phosphorus_b = QLineEdit(self.phosphorus_widget_line)
        self.phosphorus_b.setObjectName(u"phosphorus_b")

        self.horizontalLayout_11.addWidget(self.phosphorus_b)


        self.horizontalLayout_3.addWidget(self.phosphorus_widget_line)


        self.horizontalLayout_2.addWidget(self.frame_2)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.group_box_potassium = QGroupBox(self.groupBox)
        self.group_box_potassium.setObjectName(u"group_box_potassium")
        self.horizontalLayout_6 = QHBoxLayout(self.group_box_potassium)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.frame_4 = QFrame(self.group_box_potassium)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setEnabled(True)
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.potassium_combobox = QComboBox(self.frame_4)
        self.potassium_combobox.addItem("")
        self.potassium_combobox.addItem("")
        self.potassium_combobox.setObjectName(u"potassium_combobox")

        self.horizontalLayout_4.addWidget(self.potassium_combobox)

        self.potassium_widget_factor = QWidget(self.frame_4)
        self.potassium_widget_factor.setObjectName(u"potassium_widget_factor")
        self.horizontalLayout_9 = QHBoxLayout(self.potassium_widget_factor)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_2 = QLabel(self.potassium_widget_factor)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_9.addWidget(self.label_2)

        self.potassium_factor = QLineEdit(self.potassium_widget_factor)
        self.potassium_factor.setObjectName(u"potassium_factor")

        self.horizontalLayout_9.addWidget(self.potassium_factor)


        self.horizontalLayout_4.addWidget(self.potassium_widget_factor)

        self.potassium_widget_line = QWidget(self.frame_4)
        self.potassium_widget_line.setObjectName(u"potassium_widget_line")
        self.horizontalLayout_13 = QHBoxLayout(self.potassium_widget_line)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.label_6 = QLabel(self.potassium_widget_line)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_13.addWidget(self.label_6)

        self.potassium_a = QLineEdit(self.potassium_widget_line)
        self.potassium_a.setObjectName(u"potassium_a")

        self.horizontalLayout_13.addWidget(self.potassium_a)

        self.label_9 = QLabel(self.potassium_widget_line)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_13.addWidget(self.label_9)

        self.potassium_b = QLineEdit(self.potassium_widget_line)
        self.potassium_b.setObjectName(u"potassium_b")

        self.horizontalLayout_13.addWidget(self.potassium_b)


        self.horizontalLayout_4.addWidget(self.potassium_widget_line)


        self.horizontalLayout_6.addWidget(self.frame_4)


        self.verticalLayout.addWidget(self.group_box_potassium)

        self.groupBox_4 = QGroupBox(self.groupBox)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.horizontalLayout_7 = QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.frame_5 = QFrame(self.groupBox_4)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setEnabled(True)
        self.frame_5.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.organic_matter_combobox = QComboBox(self.frame_5)
        self.organic_matter_combobox.addItem("")
        self.organic_matter_combobox.addItem("")
        self.organic_matter_combobox.setObjectName(u"organic_matter_combobox")

        self.horizontalLayout_5.addWidget(self.organic_matter_combobox)

        self.organic_matter_widget_factor = QWidget(self.frame_5)
        self.organic_matter_widget_factor.setObjectName(u"organic_matter_widget_factor")
        self.horizontalLayout_10 = QHBoxLayout(self.organic_matter_widget_factor)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_3 = QLabel(self.organic_matter_widget_factor)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_10.addWidget(self.label_3)

        self.organic_matter_factor = QLineEdit(self.organic_matter_widget_factor)
        self.organic_matter_factor.setObjectName(u"organic_matter_factor")

        self.horizontalLayout_10.addWidget(self.organic_matter_factor)


        self.horizontalLayout_5.addWidget(self.organic_matter_widget_factor)


        self.horizontalLayout_7.addWidget(self.frame_5)

        self.organic_matter_widget_line = QWidget(self.groupBox_4)
        self.organic_matter_widget_line.setObjectName(u"organic_matter_widget_line")
        self.horizontalLayout_12 = QHBoxLayout(self.organic_matter_widget_line)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_5 = QLabel(self.organic_matter_widget_line)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_12.addWidget(self.label_5)

        self.organic_matter_a = QLineEdit(self.organic_matter_widget_line)
        self.organic_matter_a.setObjectName(u"organic_matter_a")

        self.horizontalLayout_12.addWidget(self.organic_matter_a)

        self.label_8 = QLabel(self.organic_matter_widget_line)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_12.addWidget(self.label_8)

        self.organic_matter_b = QLineEdit(self.organic_matter_widget_line)
        self.organic_matter_b.setObjectName(u"organic_matter_b")

        self.horizontalLayout_12.addWidget(self.organic_matter_b)


        self.horizontalLayout_7.addWidget(self.organic_matter_widget_line)


        self.verticalLayout.addWidget(self.groupBox_4)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.frame_3 = QFrame(Dialog)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMaximumSize(QSize(16777215, 50))
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout = QHBoxLayout(self.frame_3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.save_config = QPushButton(self.frame_3)
        self.save_config.setObjectName(u"save_config")
        self.save_config.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout.addWidget(self.save_config)


        self.verticalLayout_2.addWidget(self.frame_3)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Fatores Vari\u00e1veis", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Dialog", u"F\u00f3sforo", None))
        self.phosphorus_combobox.setItemText(0, QCoreApplication.translate("Dialog", u"Fator de corre\u00e7\u00e3o", None))
        self.phosphorus_combobox.setItemText(1, QCoreApplication.translate("Dialog", u"Equa\u00e7\u00e3o da Reta", None))

        self.label.setText(QCoreApplication.translate("Dialog", u"Fator (Leitura * fator):", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"y (leitura) = ax + b", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"x +", None))
        self.group_box_potassium.setTitle(QCoreApplication.translate("Dialog", u"Pot\u00e1ssio", None))
        self.potassium_combobox.setItemText(0, QCoreApplication.translate("Dialog", u"Fator de corre\u00e7\u00e3o", None))
        self.potassium_combobox.setItemText(1, QCoreApplication.translate("Dialog", u"Equa\u00e7\u00e3o da Reta", None))

        self.label_2.setText(QCoreApplication.translate("Dialog", u"Fator (Leitura * fator):", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"y (leitura) = ax + b", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"x +", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Dialog", u"Mat\u00e9ria org\u00e2nica", None))
        self.organic_matter_combobox.setItemText(0, QCoreApplication.translate("Dialog", u"Fator de corre\u00e7\u00e3o", None))
        self.organic_matter_combobox.setItemText(1, QCoreApplication.translate("Dialog", u"Equa\u00e7\u00e3o da Reta", None))

        self.label_3.setText(QCoreApplication.translate("Dialog", u"Fator (Leitura * fator):", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"y (leitura) = ax + b", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"x +", None))
        self.save_config.setText(QCoreApplication.translate("Dialog", u"Salvar", None))
    # retranslateUi

