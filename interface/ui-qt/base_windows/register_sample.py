# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'register_sample.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class RegisterSampleDialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(773, 697)
        Dialog.setMaximumSize(QSize(773, 697))
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame_33 = QFrame(Dialog)
        self.frame_33.setObjectName(u"frame_33")
        self.frame_33.setMaximumSize(QSize(16777215, 240))
        self.frame_33.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_33.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_33)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.groupBox = QGroupBox(self.frame_33)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMinimumSize(QSize(0, 0))
        self.groupBox.setMaximumSize(QSize(563, 240))
        self.horizontalLayout_7 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.frame_8 = QFrame(self.groupBox)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_8)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame_31 = QFrame(self.frame_8)
        self.frame_31.setObjectName(u"frame_31")
        self.frame_31.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_31.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_37 = QHBoxLayout(self.frame_31)
        self.horizontalLayout_37.setObjectName(u"horizontalLayout_37")
        self.frame_5 = QFrame(self.frame_31)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_5 = QLabel(self.frame_5)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_5.addWidget(self.label_5)

        self.sample_number = QLineEdit(self.frame_5)
        self.sample_number.setObjectName(u"sample_number")

        self.horizontalLayout_5.addWidget(self.sample_number)


        self.horizontalLayout_37.addWidget(self.frame_5)

        self.frame_7 = QFrame(self.frame_31)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_38 = QHBoxLayout(self.frame_7)
        self.horizontalLayout_38.setObjectName(u"horizontalLayout_38")
        self.label_3 = QLabel(self.frame_7)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_38.addWidget(self.label_3)

        self.collection_depth = QLineEdit(self.frame_7)
        self.collection_depth.setObjectName(u"collection_depth")

        self.horizontalLayout_38.addWidget(self.collection_depth)


        self.horizontalLayout_37.addWidget(self.frame_7)

        self.frame_30 = QFrame(self.frame_31)
        self.frame_30.setObjectName(u"frame_30")
        self.frame_30.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_30.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_36 = QHBoxLayout(self.frame_30)
        self.horizontalLayout_36.setObjectName(u"horizontalLayout_36")
        self.label_33 = QLabel(self.frame_30)
        self.label_33.setObjectName(u"label_33")

        self.horizontalLayout_36.addWidget(self.label_33)

        self.date = QLineEdit(self.frame_30)
        self.date.setObjectName(u"date")
        self.date.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_36.addWidget(self.date)


        self.horizontalLayout_37.addWidget(self.frame_30)


        self.verticalLayout_2.addWidget(self.frame_31)

        self.frame_2 = QFrame(self.frame_8)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.frame_32 = QFrame(self.frame_2)
        self.frame_32.setObjectName(u"frame_32")
        self.frame_32.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_32.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_39 = QHBoxLayout(self.frame_32)
        self.horizontalLayout_39.setObjectName(u"horizontalLayout_39")
        self.label_2 = QLabel(self.frame_32)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_39.addWidget(self.label_2)

        self.description = QLineEdit(self.frame_32)
        self.description.setObjectName(u"description")

        self.horizontalLayout_39.addWidget(self.description)


        self.horizontalLayout_2.addWidget(self.frame_32)

        self.frame_3 = QFrame(self.frame_2)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMaximumSize(QSize(175, 16777215))
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_6 = QLabel(self.frame_3)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_3.addWidget(self.label_6)

        self.area = QLineEdit(self.frame_3)
        self.area.setObjectName(u"area")

        self.horizontalLayout_3.addWidget(self.area)


        self.horizontalLayout_2.addWidget(self.frame_3)


        self.verticalLayout_2.addWidget(self.frame_2)

        self.frame = QFrame(self.frame_8)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame_6 = QFrame(self.frame)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label = QLabel(self.frame_6)
        self.label.setObjectName(u"label")

        self.horizontalLayout_6.addWidget(self.label)

        self.latitude = QLineEdit(self.frame_6)
        self.latitude.setObjectName(u"latitude")

        self.horizontalLayout_6.addWidget(self.latitude)


        self.horizontalLayout.addWidget(self.frame_6)

        self.frame_4 = QFrame(self.frame)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_4 = QLabel(self.frame_4)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_4.addWidget(self.label_4)

        self.longitude = QLineEdit(self.frame_4)
        self.longitude.setObjectName(u"longitude")

        self.horizontalLayout_4.addWidget(self.longitude)


        self.horizontalLayout.addWidget(self.frame_4)


        self.verticalLayout_2.addWidget(self.frame)


        self.horizontalLayout_7.addWidget(self.frame_8)


        self.horizontalLayout_9.addWidget(self.groupBox)

        self.frame_19 = QFrame(self.frame_33)
        self.frame_19.setObjectName(u"frame_19")
        self.frame_19.setMaximumSize(QSize(225, 16777215))
        self.frame_19.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_19.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_19)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.frame_9 = QFrame(self.frame_19)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_9)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_7 = QLabel(self.frame_9)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_8.addWidget(self.label_7)

        self.phosphorus = QLineEdit(self.frame_9)
        self.phosphorus.setObjectName(u"phosphorus")

        self.horizontalLayout_8.addWidget(self.phosphorus)

        self.label_8 = QLabel(self.frame_9)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_8.addWidget(self.label_8)


        self.verticalLayout_3.addWidget(self.frame_9)

        self.frame_10 = QFrame(self.frame_19)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.frame_10)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_11 = QLabel(self.frame_10)
        self.label_11.setObjectName(u"label_11")

        self.horizontalLayout_10.addWidget(self.label_11)

        self.potassium = QLineEdit(self.frame_10)
        self.potassium.setObjectName(u"potassium")

        self.horizontalLayout_10.addWidget(self.potassium)

        self.label_12 = QLabel(self.frame_10)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_10.addWidget(self.label_12)


        self.verticalLayout_3.addWidget(self.frame_10)

        self.frame_13 = QFrame(self.frame_19)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_13.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_13 = QHBoxLayout(self.frame_13)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.label_17 = QLabel(self.frame_13)
        self.label_17.setObjectName(u"label_17")

        self.horizontalLayout_13.addWidget(self.label_17)

        self.organic_matter = QLineEdit(self.frame_13)
        self.organic_matter.setObjectName(u"organic_matter")

        self.horizontalLayout_13.addWidget(self.organic_matter)

        self.label_18 = QLabel(self.frame_13)
        self.label_18.setObjectName(u"label_18")

        self.horizontalLayout_13.addWidget(self.label_18)


        self.verticalLayout_3.addWidget(self.frame_13)

        self.frame_12 = QFrame(self.frame_19)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_12.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_12 = QHBoxLayout(self.frame_12)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_15 = QLabel(self.frame_12)
        self.label_15.setObjectName(u"label_15")

        self.horizontalLayout_12.addWidget(self.label_15)

        self.ph = QLineEdit(self.frame_12)
        self.ph.setObjectName(u"ph")

        self.horizontalLayout_12.addWidget(self.ph)

        self.label_16 = QLabel(self.frame_12)
        self.label_16.setObjectName(u"label_16")

        self.horizontalLayout_12.addWidget(self.label_16)


        self.verticalLayout_3.addWidget(self.frame_12)

        self.frame_11 = QFrame(self.frame_19)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_11.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.frame_11)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_13 = QLabel(self.frame_11)
        self.label_13.setObjectName(u"label_13")

        self.horizontalLayout_11.addWidget(self.label_13)

        self.SMP = QLineEdit(self.frame_11)
        self.SMP.setObjectName(u"SMP")

        self.horizontalLayout_11.addWidget(self.SMP)

        self.label_14 = QLabel(self.frame_11)
        self.label_14.setObjectName(u"label_14")

        self.horizontalLayout_11.addWidget(self.label_14)


        self.verticalLayout_3.addWidget(self.frame_11)


        self.horizontalLayout_9.addWidget(self.frame_19)


        self.verticalLayout.addWidget(self.frame_33)

        self.groupBox_2 = QGroupBox(Dialog)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setMaximumSize(QSize(16777215, 340))
        self.horizontalLayout_20 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.frame_36 = QFrame(self.groupBox_2)
        self.frame_36.setObjectName(u"frame_36")
        self.frame_36.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_36.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_36)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.groupBox_3 = QGroupBox(self.frame_36)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setMinimumSize(QSize(0, 0))
        self.groupBox_3.setMaximumSize(QSize(400, 70))
        self.horizontalLayout_16 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.frame_14 = QFrame(self.groupBox_3)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setMinimumSize(QSize(0, 0))
        self.frame_14.setMaximumSize(QSize(100, 16777215))
        self.frame_14.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_14.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_14 = QHBoxLayout(self.frame_14)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_20 = QLabel(self.frame_14)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setMaximumSize(QSize(35, 20))

        self.horizontalLayout_14.addWidget(self.label_20)

        self.read_aluminum = QLineEdit(self.frame_14)
        self.read_aluminum.setObjectName(u"read_aluminum")
        self.read_aluminum.setMaximumSize(QSize(50, 20))

        self.horizontalLayout_14.addWidget(self.read_aluminum)


        self.horizontalLayout_16.addWidget(self.frame_14)

        self.frame_15 = QFrame(self.groupBox_3)
        self.frame_15.setObjectName(u"frame_15")
        self.frame_15.setMaximumSize(QSize(170, 16777215))
        self.frame_15.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_15.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_15 = QHBoxLayout(self.frame_15)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label_19 = QLabel(self.frame_15)
        self.label_19.setObjectName(u"label_19")

        self.horizontalLayout_15.addWidget(self.label_19)

        self.blank_test_aluminum = QLineEdit(self.frame_15)
        self.blank_test_aluminum.setObjectName(u"blank_test_aluminum")
        self.blank_test_aluminum.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_15.addWidget(self.blank_test_aluminum)


        self.horizontalLayout_16.addWidget(self.frame_15)


        self.verticalLayout_6.addWidget(self.groupBox_3)

        self.groupBox_6 = QGroupBox(self.frame_36)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.groupBox_6.setMinimumSize(QSize(0, 0))
        self.groupBox_6.setMaximumSize(QSize(400, 70))
        self.horizontalLayout_24 = QHBoxLayout(self.groupBox_6)
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.frame_22 = QFrame(self.groupBox_6)
        self.frame_22.setObjectName(u"frame_22")
        self.frame_22.setMinimumSize(QSize(0, 0))
        self.frame_22.setMaximumSize(QSize(100, 16777215))
        self.frame_22.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_22.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_25 = QHBoxLayout(self.frame_22)
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.label_25 = QLabel(self.frame_22)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setMaximumSize(QSize(35, 20))

        self.horizontalLayout_25.addWidget(self.label_25)

        self.read_copper = QLineEdit(self.frame_22)
        self.read_copper.setObjectName(u"read_copper")
        self.read_copper.setMaximumSize(QSize(50, 20))

        self.horizontalLayout_25.addWidget(self.read_copper)


        self.horizontalLayout_24.addWidget(self.frame_22)

        self.frame_23 = QFrame(self.groupBox_6)
        self.frame_23.setObjectName(u"frame_23")
        self.frame_23.setMaximumSize(QSize(170, 16777215))
        self.frame_23.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_23.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_26 = QHBoxLayout(self.frame_23)
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.label_26 = QLabel(self.frame_23)
        self.label_26.setObjectName(u"label_26")

        self.horizontalLayout_26.addWidget(self.label_26)

        self.blank_test_copper = QLineEdit(self.frame_23)
        self.blank_test_copper.setObjectName(u"blank_test_copper")
        self.blank_test_copper.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_26.addWidget(self.blank_test_copper)


        self.horizontalLayout_24.addWidget(self.frame_23)


        self.verticalLayout_6.addWidget(self.groupBox_6)

        self.groupBox_4 = QGroupBox(self.frame_36)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setMinimumSize(QSize(0, 0))
        self.groupBox_4.setMaximumSize(QSize(400, 70))
        self.horizontalLayout_17 = QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.frame_16 = QFrame(self.groupBox_4)
        self.frame_16.setObjectName(u"frame_16")
        self.frame_16.setMinimumSize(QSize(0, 0))
        self.frame_16.setMaximumSize(QSize(100, 16777215))
        self.frame_16.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_16.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_18 = QHBoxLayout(self.frame_16)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.label_21 = QLabel(self.frame_16)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setMaximumSize(QSize(35, 20))

        self.horizontalLayout_18.addWidget(self.label_21)

        self.read_calcium = QLineEdit(self.frame_16)
        self.read_calcium.setObjectName(u"read_calcium")
        self.read_calcium.setMaximumSize(QSize(50, 20))

        self.horizontalLayout_18.addWidget(self.read_calcium)


        self.horizontalLayout_17.addWidget(self.frame_16)

        self.frame_17 = QFrame(self.groupBox_4)
        self.frame_17.setObjectName(u"frame_17")
        self.frame_17.setMaximumSize(QSize(170, 16777215))
        self.frame_17.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_17.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_19 = QHBoxLayout(self.frame_17)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.label_22 = QLabel(self.frame_17)
        self.label_22.setObjectName(u"label_22")

        self.horizontalLayout_19.addWidget(self.label_22)

        self.blank_test_calcium = QLineEdit(self.frame_17)
        self.blank_test_calcium.setObjectName(u"blank_test_calcium")
        self.blank_test_calcium.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_19.addWidget(self.blank_test_calcium)


        self.horizontalLayout_17.addWidget(self.frame_17)


        self.verticalLayout_6.addWidget(self.groupBox_4)


        self.horizontalLayout_20.addWidget(self.frame_36)

        self.frame_18 = QFrame(self.groupBox_2)
        self.frame_18.setObjectName(u"frame_18")
        self.frame_18.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_18.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_18)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.groupBox_5 = QGroupBox(self.frame_18)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setMinimumSize(QSize(0, 0))
        self.groupBox_5.setMaximumSize(QSize(400, 70))
        self.horizontalLayout_21 = QHBoxLayout(self.groupBox_5)
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.frame_20 = QFrame(self.groupBox_5)
        self.frame_20.setObjectName(u"frame_20")
        self.frame_20.setMinimumSize(QSize(0, 0))
        self.frame_20.setMaximumSize(QSize(100, 16777215))
        self.frame_20.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_20.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_22 = QHBoxLayout(self.frame_20)
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.label_23 = QLabel(self.frame_20)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setMaximumSize(QSize(35, 20))

        self.horizontalLayout_22.addWidget(self.label_23)

        self.read_magnesium = QLineEdit(self.frame_20)
        self.read_magnesium.setObjectName(u"read_magnesium")
        self.read_magnesium.setMaximumSize(QSize(50, 20))

        self.horizontalLayout_22.addWidget(self.read_magnesium)


        self.horizontalLayout_21.addWidget(self.frame_20)

        self.frame_21 = QFrame(self.groupBox_5)
        self.frame_21.setObjectName(u"frame_21")
        self.frame_21.setMaximumSize(QSize(170, 16777215))
        self.frame_21.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_21.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_23 = QHBoxLayout(self.frame_21)
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.label_24 = QLabel(self.frame_21)
        self.label_24.setObjectName(u"label_24")

        self.horizontalLayout_23.addWidget(self.label_24)

        self.blank_test_magnesium = QLineEdit(self.frame_21)
        self.blank_test_magnesium.setObjectName(u"blank_test_magnesium")
        self.blank_test_magnesium.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_23.addWidget(self.blank_test_magnesium)


        self.horizontalLayout_21.addWidget(self.frame_21)


        self.verticalLayout_5.addWidget(self.groupBox_5)

        self.groupBox_7 = QGroupBox(self.frame_18)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.groupBox_7.setMinimumSize(QSize(0, 0))
        self.groupBox_7.setMaximumSize(QSize(400, 70))
        self.horizontalLayout_27 = QHBoxLayout(self.groupBox_7)
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.frame_24 = QFrame(self.groupBox_7)
        self.frame_24.setObjectName(u"frame_24")
        self.frame_24.setMinimumSize(QSize(0, 0))
        self.frame_24.setMaximumSize(QSize(100, 16777215))
        self.frame_24.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_24.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_28 = QHBoxLayout(self.frame_24)
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.label_27 = QLabel(self.frame_24)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setMaximumSize(QSize(35, 20))

        self.horizontalLayout_28.addWidget(self.label_27)

        self.read_iron = QLineEdit(self.frame_24)
        self.read_iron.setObjectName(u"read_iron")
        self.read_iron.setMaximumSize(QSize(50, 20))

        self.horizontalLayout_28.addWidget(self.read_iron)


        self.horizontalLayout_27.addWidget(self.frame_24)

        self.frame_25 = QFrame(self.groupBox_7)
        self.frame_25.setObjectName(u"frame_25")
        self.frame_25.setMaximumSize(QSize(170, 16777215))
        self.frame_25.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_25.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_29 = QHBoxLayout(self.frame_25)
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.label_28 = QLabel(self.frame_25)
        self.label_28.setObjectName(u"label_28")

        self.horizontalLayout_29.addWidget(self.label_28)

        self.blank_test_iron = QLineEdit(self.frame_25)
        self.blank_test_iron.setObjectName(u"blank_test_iron")
        self.blank_test_iron.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_29.addWidget(self.blank_test_iron)


        self.horizontalLayout_27.addWidget(self.frame_25)


        self.verticalLayout_5.addWidget(self.groupBox_7)

        self.groupBox_8 = QGroupBox(self.frame_18)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.groupBox_8.setMinimumSize(QSize(0, 0))
        self.groupBox_8.setMaximumSize(QSize(400, 70))
        self.horizontalLayout_30 = QHBoxLayout(self.groupBox_8)
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.frame_26 = QFrame(self.groupBox_8)
        self.frame_26.setObjectName(u"frame_26")
        self.frame_26.setMinimumSize(QSize(0, 0))
        self.frame_26.setMaximumSize(QSize(100, 16777215))
        self.frame_26.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_26.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_31 = QHBoxLayout(self.frame_26)
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.label_29 = QLabel(self.frame_26)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setMaximumSize(QSize(35, 20))

        self.horizontalLayout_31.addWidget(self.label_29)

        self.read_manganese = QLineEdit(self.frame_26)
        self.read_manganese.setObjectName(u"read_manganese")
        self.read_manganese.setMaximumSize(QSize(50, 20))

        self.horizontalLayout_31.addWidget(self.read_manganese)


        self.horizontalLayout_30.addWidget(self.frame_26)

        self.frame_27 = QFrame(self.groupBox_8)
        self.frame_27.setObjectName(u"frame_27")
        self.frame_27.setMaximumSize(QSize(170, 16777215))
        self.frame_27.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_27.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_32 = QHBoxLayout(self.frame_27)
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.label_30 = QLabel(self.frame_27)
        self.label_30.setObjectName(u"label_30")

        self.horizontalLayout_32.addWidget(self.label_30)

        self.blank_test_manganese = QLineEdit(self.frame_27)
        self.blank_test_manganese.setObjectName(u"blank_test_manganese")
        self.blank_test_manganese.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_32.addWidget(self.blank_test_manganese)


        self.horizontalLayout_30.addWidget(self.frame_27)


        self.verticalLayout_5.addWidget(self.groupBox_8)

        self.groupBox_9 = QGroupBox(self.frame_18)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.groupBox_9.setMinimumSize(QSize(0, 0))
        self.groupBox_9.setMaximumSize(QSize(400, 70))
        self.horizontalLayout_33 = QHBoxLayout(self.groupBox_9)
        self.horizontalLayout_33.setObjectName(u"horizontalLayout_33")
        self.frame_28 = QFrame(self.groupBox_9)
        self.frame_28.setObjectName(u"frame_28")
        self.frame_28.setMinimumSize(QSize(0, 0))
        self.frame_28.setMaximumSize(QSize(100, 16777215))
        self.frame_28.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_28.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_34 = QHBoxLayout(self.frame_28)
        self.horizontalLayout_34.setObjectName(u"horizontalLayout_34")
        self.label_31 = QLabel(self.frame_28)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setMaximumSize(QSize(35, 20))

        self.horizontalLayout_34.addWidget(self.label_31)

        self.read_zinc = QLineEdit(self.frame_28)
        self.read_zinc.setObjectName(u"read_zinc")
        self.read_zinc.setMaximumSize(QSize(50, 20))

        self.horizontalLayout_34.addWidget(self.read_zinc)


        self.horizontalLayout_33.addWidget(self.frame_28)

        self.frame_29 = QFrame(self.groupBox_9)
        self.frame_29.setObjectName(u"frame_29")
        self.frame_29.setMaximumSize(QSize(170, 16777215))
        self.frame_29.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_29.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_35 = QHBoxLayout(self.frame_29)
        self.horizontalLayout_35.setObjectName(u"horizontalLayout_35")
        self.label_32 = QLabel(self.frame_29)
        self.label_32.setObjectName(u"label_32")

        self.horizontalLayout_35.addWidget(self.label_32)

        self.blank_test_zinc = QLineEdit(self.frame_29)
        self.blank_test_zinc.setObjectName(u"blank_test_zinc")
        self.blank_test_zinc.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_35.addWidget(self.blank_test_zinc)


        self.horizontalLayout_33.addWidget(self.frame_29)


        self.verticalLayout_5.addWidget(self.groupBox_9)


        self.horizontalLayout_20.addWidget(self.frame_18)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.frame_34 = QFrame(Dialog)
        self.frame_34.setObjectName(u"frame_34")
        self.frame_34.setMaximumSize(QSize(16777215, 45))
        self.frame_34.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_34.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_40 = QHBoxLayout(self.frame_34)
        self.horizontalLayout_40.setObjectName(u"horizontalLayout_40")
        self.register_button = QPushButton(self.frame_34)
        self.register_button.setObjectName(u"register_button")
        self.register_button.setMaximumSize(QSize(150, 16777215))

        self.horizontalLayout_40.addWidget(self.register_button)


        self.verticalLayout.addWidget(self.frame_34)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Dados da amostra", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"N\u00ba amostra:", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Profundidade (cm):", None))
        self.label_33.setText(QCoreApplication.translate("Dialog", u"Data:", None))
        self.date.setInputMask(QCoreApplication.translate("Dialog", u"99/99/9999", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Descri\u00e7\u00e3o:", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"\u00c1rea total (m\u00b2):", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Latitude:", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Longitude:", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"F\u00f3sforo (P)", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"mg/dm-\u00b3", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"Pot\u00e1ssio (K)", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"cmol/dm-\u00b3", None))
        self.label_17.setText(QCoreApplication.translate("Dialog", u"MO", None))
        self.label_18.setText(QCoreApplication.translate("Dialog", u"g/dm-\u00b3", None))
        self.label_15.setText(QCoreApplication.translate("Dialog", u"pH CaCl\u00b2", None))
        self.label_16.setText("")
        self.label_13.setText(QCoreApplication.translate("Dialog", u"\u00cdndice SMP", None))
        self.label_14.setText("")
        self.groupBox_2.setTitle(QCoreApplication.translate("Dialog", u"Valores de medi\u00e7\u00e3o", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Dialog", u"Alum\u00ednio (Al) - cmol/dm-\u00b3", None))
        self.label_20.setText(QCoreApplication.translate("Dialog", u"Leitura:", None))
        self.label_19.setText(QCoreApplication.translate("Dialog", u"Prova em branco:", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("Dialog", u"Cobre (Cu) - mg/dm-\u00b3", None))
        self.label_25.setText(QCoreApplication.translate("Dialog", u"Leitura:", None))
        self.label_26.setText(QCoreApplication.translate("Dialog", u"Prova em branco:", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Dialog", u"C\u00e1lcio (Ca) - cmol/dm-\u00b3", None))
        self.label_21.setText(QCoreApplication.translate("Dialog", u"Leitura:", None))
        self.label_22.setText(QCoreApplication.translate("Dialog", u"Prova em branco:", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("Dialog", u"Magn\u00e9sio (Mg) - cmol/dm-\u00b3", None))
        self.label_23.setText(QCoreApplication.translate("Dialog", u"Leitura:", None))
        self.label_24.setText(QCoreApplication.translate("Dialog", u"Prova em branco:", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("Dialog", u"Ferro (Fe) - mg/dm-\u00b3", None))
        self.label_27.setText(QCoreApplication.translate("Dialog", u"Leitura:", None))
        self.label_28.setText(QCoreApplication.translate("Dialog", u"Prova em branco:", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("Dialog", u"Mangan\u00eas (Mn)  - mg/dm-\u00b3", None))
        self.label_29.setText(QCoreApplication.translate("Dialog", u"Leitura:", None))
        self.label_30.setText(QCoreApplication.translate("Dialog", u"Prova em branco:", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("Dialog", u"Zinco (Zn) - mg/dm-\u00b3", None))
        self.label_31.setText(QCoreApplication.translate("Dialog", u"Leitura:", None))
        self.label_32.setText(QCoreApplication.translate("Dialog", u"Prova em branco:", None))
        self.register_button.setText(QCoreApplication.translate("Dialog", u"Registrar", None))
    # retranslateUi

