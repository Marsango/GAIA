# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'upload_logo.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class UploadLogoDialog(object):
    def setupUi(self, UploadLogo):
        if not UploadLogo.objectName():
            UploadLogo.setObjectName(u"UploadLogo")
        UploadLogo.resize(732, 609)
        self.horizontalLayout = QHBoxLayout(UploadLogo)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame = QFrame(UploadLogo)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_2 = QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.verticalLayout_3 = QVBoxLayout(self.frame_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_2 = QLabel(self.frame_3)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_3.addWidget(self.label_2)

        self.image_label = QLabel(self.frame_3)
        self.image_label.setObjectName(u"image_label")
        self.image_label.setMinimumSize(QSize(500, 500))
        self.image_label.setPixmap(QPixmap(u"../images/logo_lab.png"))

        self.verticalLayout_3.addWidget(self.image_label)


        self.horizontalLayout_2.addWidget(self.frame_3)

        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMaximumSize(QSize(275, 16777215))
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.verticalLayout = QVBoxLayout(self.frame_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.instruction = QLabel(self.frame_2)
        self.instruction.setObjectName(u"instruction")
        font = QFont()
        font.setPointSize(15)
        self.instruction.setFont(font)
        self.instruction.setLayoutDirection(Qt.LeftToRight)
        self.instruction.setScaledContents(False)
        self.instruction.setAlignment(Qt.AlignCenter)
        self.instruction.setWordWrap(True)

        self.verticalLayout.addWidget(self.instruction)

        self.frame_6 = QFrame(self.frame_2)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMaximumSize(QSize(275, 150))
        self.frame_6.setFrameShape(QFrame.NoFrame)
        self.verticalLayout_2 = QVBoxLayout(self.frame_6)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.file_path = QLineEdit(self.frame_6)
        self.file_path.setObjectName(u"file_path")

        self.verticalLayout_2.addWidget(self.file_path)

        self.upload_button = QPushButton(self.frame_6)
        self.upload_button.setObjectName(u"upload_button")

        self.verticalLayout_2.addWidget(self.upload_button)

        self.save_button = QPushButton(self.frame_6)
        self.save_button.setObjectName(u"save_button")

        self.verticalLayout_2.addWidget(self.save_button)


        self.verticalLayout.addWidget(self.frame_6)


        self.horizontalLayout_2.addWidget(self.frame_2)


        self.horizontalLayout.addWidget(self.frame)


        self.retranslateUi(UploadLogo)

        QMetaObject.connectSlotsByName(UploadLogo)
    # setupUi

    def retranslateUi(self, UploadLogo):
        UploadLogo.setWindowTitle(QCoreApplication.translate("UploadLogo", u"Dialog", None))
        self.label_2.setText(QCoreApplication.translate("UploadLogo", u"Logo atual", None))
        self.image_label.setText("")
        self.instruction.setText(QCoreApplication.translate("UploadLogo", u"Para uma melhor qualidade, sugere-se o tamanho da imagem 500x500px e fundo transparente.", None))
        self.upload_button.setText(QCoreApplication.translate("UploadLogo", u"Upload", None))
        self.save_button.setText(QCoreApplication.translate("UploadLogo", u"Salvar", None))
    # retranslateUi

