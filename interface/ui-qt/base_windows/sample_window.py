# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sample_window.ui'
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
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class SampleDialog(object):
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
        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.frame_3)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.owner = QLineEdit(self.frame_3)
        self.owner.setObjectName(u"owner")
        self.owner.setReadOnly(True)

        self.horizontalLayout_2.addWidget(self.owner)


        self.verticalLayout_2.addWidget(self.frame_3)

        self.frame_4 = QFrame(self.frame)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_2 = QLabel(self.frame_4)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_3.addWidget(self.label_2)

        self._property = QLineEdit(self.frame_4)
        self._property.setObjectName(u"property")
        self._property.setReadOnly(True)

        self.horizontalLayout_3.addWidget(self._property)


        self.verticalLayout_2.addWidget(self.frame_4)

        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(720, 46))
        self.frame_2.setMaximumSize(QSize(625, 30))
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout = QHBoxLayout(self.frame_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.generate_report = QPushButton(self.frame_2)
        self.generate_report.setObjectName(u"generate_report")
        self.generate_report.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout.addWidget(self.generate_report)

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

        self.property_table = QTableWidget(self.frame)
        if (self.property_table.columnCount() < 5):
            self.property_table.setColumnCount(5)
        font = QFont()
        font.setPointSize(8)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setFont(font);
        self.property_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.property_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.property_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.property_table.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.property_table.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.property_table.setObjectName(u"property_table")
        self.property_table.horizontalHeader().setDefaultSectionSize(142)

        self.verticalLayout_2.addWidget(self.property_table)


        self.verticalLayout.addWidget(self.frame)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Propriet\u00e1rio:", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Propriedade:", None))
        self.generate_report.setText(QCoreApplication.translate("Dialog", u"Gerar Laudo", None))
        self.add.setText(QCoreApplication.translate("Dialog", u"Adicionar", None))
        self.edit.setText(QCoreApplication.translate("Dialog", u"Editar", None))
        self.delete_2.setText(QCoreApplication.translate("Dialog", u"Excluir", None))
        ___qtablewidgetitem = self.property_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"id", None));
        ___qtablewidgetitem1 = self.property_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"N\u00ba da amostra", None));
        ___qtablewidgetitem2 = self.property_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Dialog", u"Descri\u00e7\u00e3o", None));
        ___qtablewidgetitem3 = self.property_table.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Dialog", u"Profundidade", None));
        ___qtablewidgetitem4 = self.property_table.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Dialog", u"Data", None));
    # retranslateUi

