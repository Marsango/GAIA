# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'backup_window.ui'
##
## Created by: Qt User Interface Compiler version 6.7.3
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QFrame,
                               QHBoxLayout, QLabel, QLineEdit, QPushButton,
                               QSizePolicy, QVBoxLayout, QWidget)


class BackupDialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 300)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMaximumSize(QSize(175, 16777215))
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.frame_3 = QFrame(self.frame_2)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.frame_3)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.requester_count = QLineEdit(self.frame_3)
        self.requester_count.setObjectName(u"requester_count")
        self.requester_count.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout.addWidget(self.requester_count)

        self.verticalLayout_3.addWidget(self.frame_3)

        self.frame_4 = QFrame(self.frame_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.frame_4)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.property_count = QLineEdit(self.frame_4)
        self.property_count.setObjectName(u"property_count")
        self.property_count.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_2.addWidget(self.property_count)

        self.verticalLayout_3.addWidget(self.frame_4)

        self.frame_5 = QFrame(self.frame_2)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_3 = QLabel(self.frame_5)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_3.addWidget(self.label_3)

        self.sample_count = QLineEdit(self.frame_5)
        self.sample_count.setObjectName(u"sample_count")
        self.sample_count.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_3.addWidget(self.sample_count)

        self.verticalLayout_3.addWidget(self.frame_5)

        self.horizontalLayout_4.addWidget(self.frame_2)

        self.frame_6 = QFrame(self.frame)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_6)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.backup_checkbox = QCheckBox(self.frame_6)
        self.backup_checkbox.setObjectName(u"backup_checkbox")

        self.verticalLayout_2.addWidget(self.backup_checkbox)

        self.frame_7 = QFrame(self.frame_6)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setMaximumSize(QSize(16777215, 40))
        self.frame_7.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_7)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_4 = QLabel(self.frame_7)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_5.addWidget(self.label_4)

        self.backup_path = QLineEdit(self.frame_7)
        self.backup_path.setObjectName(u"backup_path")

        self.horizontalLayout_5.addWidget(self.backup_path)

        self.verticalLayout_2.addWidget(self.frame_7)

        self.select_folder = QPushButton(self.frame_6)
        self.select_folder.setObjectName(u"select_folder")

        self.verticalLayout_2.addWidget(self.select_folder)

        self.horizontalLayout_4.addWidget(self.frame_6)

        self.verticalLayout.addWidget(self.frame)

        self.backup_button = QPushButton(Dialog)
        self.backup_button.setObjectName(u"backup_button")

        self.verticalLayout.addWidget(self.backup_button)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)

    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Solicitantes:", None))
        self.requester_count.setText("")
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Propridades:", None))
        self.property_count.setText("")
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Amostras:", None))
        self.sample_count.setText("")
        self.backup_checkbox.setText(QCoreApplication.translate("Dialog", u"Fazer backup dos laudos", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Pasta:", None))
        self.select_folder.setText(QCoreApplication.translate("Dialog", u"Selecionar pasta", None))
        self.backup_button.setText(QCoreApplication.translate("Dialog", u"Fazer backup", None))
    # retranslateUi
