# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'information_window.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class InformationWindowDialog(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(509, 301)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.ok_button = QPushButton(self.frame)
        self.ok_button.setObjectName(u"ok_button")
        self.ok_button.setMaximumSize(QSize(100, 16777215))
        self.ok_button.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.ok_button)


        self.verticalLayout.addWidget(self.frame)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"center\">Explica\u00e7\u00e3o:</p><p>Na configura\u00e7\u00e3o dos par\u00e2metros, h\u00e1 as colunas muito baixo, baixo, m\u00e9dio, alto e muito alto.</p><p>Se valor &lt; muito baixo, ent\u00e3o muito baixo.</p><p>Se valor  &gt;= muito baixo e  valor &lt; baixo, ent\u00e3o baixo.</p><p>Se valor &gt;= baixo e valor &lt; m\u00e9dio, ent\u00e3o m\u00e9dio.</p><p>Se valor &gt;= m\u00e9dio e &lt; alto, ent\u00e3o alto.</p><p>Se valor &gt;= alto, ent\u00e3o muito alto.</p><p>O valor muito alto em teoria n\u00e3o precisa definir, mas o software acusar\u00e1 erro caso n\u00e3o defina.</p></body></html>", None))
        self.ok_button.setText(QCoreApplication.translate("Form", u"Ok!", None))
    # retranslateUi

