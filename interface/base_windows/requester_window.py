# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'requester_window.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QHBoxLayout, QHeaderView, QPushButton, QSizePolicy,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class RequesterDialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(750, 441)
        Dialog.setMinimumSize(QSize(750, 441))
        Dialog.setMaximumSize(QSize(750, 441))
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(712, 0))
        self.frame.setFrameShape(QFrame.NoFrame)
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(720, 46))
        self.frame_2.setMaximumSize(QSize(625, 30))
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout = QHBoxLayout(self.frame_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.requester_type = QComboBox(self.frame_2)
        self.requester_type.addItem("")
        self.requester_type.addItem("")
        self.requester_type.setObjectName(u"requester_type")
        self.requester_type.setMinimumSize(QSize(50, 0))
        self.requester_type.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout.addWidget(self.requester_type)

        self.register_property = QPushButton(self.frame_2)
        self.register_property.setObjectName(u"register_property")
        self.register_property.setMaximumSize(QSize(125, 16777215))

        self.horizontalLayout.addWidget(self.register_property)

        self.add = QPushButton(self.frame_2)
        self.add.setObjectName(u"add")
        self.add.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout.addWidget(self.add)

        self.edit = QPushButton(self.frame_2)
        self.edit.setObjectName(u"edit")
        self.edit.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout.addWidget(self.edit)

        self.delete_2 = QPushButton(self.frame_2)
        self.delete_2.setObjectName(u"delete_2")
        self.delete_2.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout.addWidget(self.delete_2)


        self.verticalLayout_2.addWidget(self.frame_2)

        self.requester_table = QTableWidget(self.frame)
        if (self.requester_table.columnCount() < 7):
            self.requester_table.setColumnCount(7)
        __qtablewidgetitem = QTableWidgetItem()
        self.requester_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.requester_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.requester_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.requester_table.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.requester_table.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.requester_table.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.requester_table.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        self.requester_table.setObjectName(u"requester_table")

        self.verticalLayout_2.addWidget(self.requester_table)


        self.verticalLayout.addWidget(self.frame)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.requester_type.setItemText(0, QCoreApplication.translate("Dialog", u"Pessoa f\u00edsica", None))
        self.requester_type.setItemText(1, QCoreApplication.translate("Dialog", u"Pessoa jur\u00eddica", None))

        self.register_property.setText(QCoreApplication.translate("Dialog", u"Ver propriedades", None))
        self.add.setText(QCoreApplication.translate("Dialog", u"Adicionar", None))
        self.edit.setText(QCoreApplication.translate("Dialog", u"Editar", None))
        self.delete_2.setText(QCoreApplication.translate("Dialog", u"Excluir", None))
        ___qtablewidgetitem = self.requester_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"id", None));
        ___qtablewidgetitem1 = self.requester_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"Nome", None));
        ___qtablewidgetitem2 = self.requester_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Dialog", u"Nascimento", None));
        ___qtablewidgetitem3 = self.requester_table.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Dialog", u"CPF", None));
        ___qtablewidgetitem4 = self.requester_table.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Dialog", u"Telefone", None));
        ___qtablewidgetitem5 = self.requester_table.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Dialog", u"E-mail", None));
        ___qtablewidgetitem6 = self.requester_table.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Dialog", u"Endere\u00e7o", None));
    # retranslateUi

