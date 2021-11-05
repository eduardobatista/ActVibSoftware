# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ControlPanel.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_ControlForm(object):
    def setupUi(self, ControlForm):
        if not ControlForm.objectName():
            ControlForm.setObjectName(u"ControlForm")
        ControlForm.resize(481, 190)
        self.horizontalLayout = QHBoxLayout(ControlForm)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.Controle = QFrame(ControlForm)
        self.Controle.setObjectName(u"Controle")
        self.Controle.setAutoFillBackground(False)
        self.Controle.setStyleSheet(u"")
        self.Controle.setFrameShape(QFrame.NoFrame)
        self.Controle.setFrameShadow(QFrame.Plain)
        self.Controle.setLineWidth(0)
        self.horizontalLayout_5 = QHBoxLayout(self.Controle)
        self.horizontalLayout_5.setSpacing(2)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(5, 5, 0, 5)
        self.checkControle = QCheckBox(self.Controle)
        self.checkControle.setObjectName(u"checkControle")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkControle.sizePolicy().hasHeightForWidth())
        self.checkControle.setSizePolicy(sizePolicy)

        self.horizontalLayout_5.addWidget(self.checkControle)

        self.line = QFrame(self.Controle)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_5.addWidget(self.line)

        self.frame_7 = QFrame(self.Controle)
        self.frame_7.setObjectName(u"frame_7")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame_7.sizePolicy().hasHeightForWidth())
        self.frame_7.setSizePolicy(sizePolicy1)
        self.frame_7.setMinimumSize(QSize(0, 150))
        self.frame_7.setFrameShadow(QFrame.Sunken)
        self.frame_7.setLineWidth(0)
        self.gridLayout_2 = QGridLayout(self.frame_7)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setVerticalSpacing(2)
        self.gridLayout_2.setContentsMargins(3, 1, 5, 1)
        self.label_11 = QLabel(self.frame_7)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_2.addWidget(self.label_11, 8, 5, 1, 2)

        self.checkAlgOn = QCheckBox(self.frame_7)
        self.checkAlgOn.setObjectName(u"checkAlgOn")

        self.gridLayout_2.addWidget(self.checkAlgOn, 4, 4, 1, 2)

        self.spinTAlgOn = QSpinBox(self.frame_7)
        self.spinTAlgOn.setObjectName(u"spinTAlgOn")

        self.gridLayout_2.addWidget(self.spinTAlgOn, 4, 6, 1, 1)

        self.comboIMURef = QComboBox(self.frame_7)
        self.comboIMURef.addItem("")
        self.comboIMURef.addItem("")
        self.comboIMURef.addItem("")
        self.comboIMURef.setObjectName(u"comboIMURef")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.comboIMURef.sizePolicy().hasHeightForWidth())
        self.comboIMURef.setSizePolicy(sizePolicy2)

        self.gridLayout_2.addWidget(self.comboIMURef, 2, 4, 1, 3)

        self.normCtrl = QLineEdit(self.frame_7)
        self.normCtrl.setObjectName(u"normCtrl")

        self.gridLayout_2.addWidget(self.normCtrl, 8, 7, 1, 1)

        self.label_17 = QLabel(self.frame_7)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_17, 3, 3, 1, 1)

        self.label_8 = QLabel(self.frame_7)
        self.label_8.setObjectName(u"label_8")
        sizePolicy2.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy2)
        self.label_8.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.label_8.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_8, 4, 3, 1, 1)

        self.label_24 = QLabel(self.frame_7)
        self.label_24.setObjectName(u"label_24")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_24.sizePolicy().hasHeightForWidth())
        self.label_24.setSizePolicy(sizePolicy3)
        self.label_24.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_24, 0, 3, 1, 1)

        self.label_48 = QLabel(self.frame_7)
        self.label_48.setObjectName(u"label_48")
        sizePolicy3.setHeightForWidth(self.label_48.sizePolicy().hasHeightForWidth())
        self.label_48.setSizePolicy(sizePolicy3)
        self.label_48.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_48, 1, 3, 1, 1)

        self.line_3 = QFrame(self.frame_7)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.gridLayout_2.addWidget(self.line_3, 5, 4, 4, 1)

        self.label_16 = QLabel(self.frame_7)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_16, 2, 3, 1, 1)

        self.comboIMUError = QComboBox(self.frame_7)
        self.comboIMUError.addItem("")
        self.comboIMUError.addItem("")
        self.comboIMUError.addItem("")
        self.comboIMUError.setObjectName(u"comboIMUError")
        sizePolicy2.setHeightForWidth(self.comboIMUError.sizePolicy().hasHeightForWidth())
        self.comboIMUError.setSizePolicy(sizePolicy2)

        self.gridLayout_2.addWidget(self.comboIMUError, 3, 4, 1, 3)

        self.spinMemCtrl = QSpinBox(self.frame_7)
        self.spinMemCtrl.setObjectName(u"spinMemCtrl")
        self.spinMemCtrl.setMinimum(1)
        self.spinMemCtrl.setMaximum(3000)
        self.spinMemCtrl.setValue(100)

        self.gridLayout_2.addWidget(self.spinMemCtrl, 6, 7, 1, 1)

        self.label_9 = QLabel(self.frame_7)
        self.label_9.setObjectName(u"label_9")
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)

        self.gridLayout_2.addWidget(self.label_9, 7, 5, 1, 2)

        self.comboControlChannel = QComboBox(self.frame_7)
        self.comboControlChannel.addItem("")
        self.comboControlChannel.addItem("")
        self.comboControlChannel.addItem("")
        self.comboControlChannel.addItem("")
        self.comboControlChannel.setObjectName(u"comboControlChannel")
        sizePolicy2.setHeightForWidth(self.comboControlChannel.sizePolicy().hasHeightForWidth())
        self.comboControlChannel.setSizePolicy(sizePolicy2)

        self.gridLayout_2.addWidget(self.comboControlChannel, 1, 4, 1, 4)

        self.comboRef = QComboBox(self.frame_7)
        self.comboRef.addItem("")
        self.comboRef.addItem("")
        self.comboRef.addItem("")
        self.comboRef.addItem("")
        self.comboRef.addItem("")
        self.comboRef.addItem("")
        self.comboRef.setObjectName(u"comboRef")
        sizePolicy2.setHeightForWidth(self.comboRef.sizePolicy().hasHeightForWidth())
        self.comboRef.setSizePolicy(sizePolicy2)

        self.gridLayout_2.addWidget(self.comboRef, 2, 7, 1, 1)

        self.label_12 = QLabel(self.frame_7)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_2.addWidget(self.label_12, 6, 5, 1, 2)

        self.comboErro = QComboBox(self.frame_7)
        self.comboErro.addItem("")
        self.comboErro.addItem("")
        self.comboErro.addItem("")
        self.comboErro.addItem("")
        self.comboErro.addItem("")
        self.comboErro.addItem("")
        self.comboErro.setObjectName(u"comboErro")
        sizePolicy2.setHeightForWidth(self.comboErro.sizePolicy().hasHeightForWidth())
        self.comboErro.setSizePolicy(sizePolicy2)

        self.gridLayout_2.addWidget(self.comboErro, 3, 7, 1, 1)

        self.comboAlgoritmo = QComboBox(self.frame_7)
        self.comboAlgoritmo.addItem("")
        self.comboAlgoritmo.addItem("")
        self.comboAlgoritmo.addItem("")
        self.comboAlgoritmo.setObjectName(u"comboAlgoritmo")

        self.gridLayout_2.addWidget(self.comboAlgoritmo, 4, 7, 1, 1)

        self.passoCtrl = QLineEdit(self.frame_7)
        self.passoCtrl.setObjectName(u"passoCtrl")

        self.gridLayout_2.addWidget(self.passoCtrl, 7, 7, 1, 1)

        self.label_10 = QLabel(self.frame_7)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_10, 6, 3, 3, 1)

        self.comboPerturbChannel = QComboBox(self.frame_7)
        self.comboPerturbChannel.addItem("")
        self.comboPerturbChannel.addItem("")
        self.comboPerturbChannel.addItem("")
        self.comboPerturbChannel.addItem("")
        self.comboPerturbChannel.setObjectName(u"comboPerturbChannel")
        sizePolicy2.setHeightForWidth(self.comboPerturbChannel.sizePolicy().hasHeightForWidth())
        self.comboPerturbChannel.setSizePolicy(sizePolicy2)

        self.gridLayout_2.addWidget(self.comboPerturbChannel, 0, 4, 1, 4)


        self.horizontalLayout_5.addWidget(self.frame_7)

        self.line_4 = QFrame(self.Controle)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.VLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_5.addWidget(self.line_4)


        self.horizontalLayout.addWidget(self.Controle)

        QWidget.setTabOrder(self.checkControle, self.comboPerturbChannel)
        QWidget.setTabOrder(self.comboPerturbChannel, self.comboControlChannel)
        QWidget.setTabOrder(self.comboControlChannel, self.comboIMURef)
        QWidget.setTabOrder(self.comboIMURef, self.comboRef)
        QWidget.setTabOrder(self.comboRef, self.comboIMUError)
        QWidget.setTabOrder(self.comboIMUError, self.comboErro)
        QWidget.setTabOrder(self.comboErro, self.checkAlgOn)
        QWidget.setTabOrder(self.checkAlgOn, self.spinTAlgOn)
        QWidget.setTabOrder(self.spinTAlgOn, self.comboAlgoritmo)
        QWidget.setTabOrder(self.comboAlgoritmo, self.spinMemCtrl)
        QWidget.setTabOrder(self.spinMemCtrl, self.passoCtrl)
        QWidget.setTabOrder(self.passoCtrl, self.normCtrl)

        self.retranslateUi(ControlForm)

        QMetaObject.connectSlotsByName(ControlForm)
    # setupUi

    def retranslateUi(self, ControlForm):
        ControlForm.setWindowTitle(QCoreApplication.translate("ControlForm", u"Form", None))
        self.checkControle.setText(QCoreApplication.translate("ControlForm", u"Enable", None))
        self.label_11.setText(QCoreApplication.translate("ControlForm", u"Penalization:", None))
        self.checkAlgOn.setText(QCoreApplication.translate("ControlForm", u"On \u2265", None))
        self.comboIMURef.setItemText(0, QCoreApplication.translate("ControlForm", u"IMU 1", None))
        self.comboIMURef.setItemText(1, QCoreApplication.translate("ControlForm", u"IMU 2", None))
        self.comboIMURef.setItemText(2, QCoreApplication.translate("ControlForm", u"IMU 3", None))

        self.normCtrl.setText(QCoreApplication.translate("ControlForm", u"1e-4", None))
        self.label_17.setText(QCoreApplication.translate("ControlForm", u"Error Sensor:", None))
        self.label_8.setText(QCoreApplication.translate("ControlForm", u"Algorithm:", None))
        self.label_24.setText(QCoreApplication.translate("ControlForm", u"Perturbation:", None))
        self.label_48.setText(QCoreApplication.translate("ControlForm", u"Control:", None))
        self.label_16.setText(QCoreApplication.translate("ControlForm", u"Ref. Sensor:", None))
        self.comboIMUError.setItemText(0, QCoreApplication.translate("ControlForm", u"IMU 1", None))
        self.comboIMUError.setItemText(1, QCoreApplication.translate("ControlForm", u"IMU 2", None))
        self.comboIMUError.setItemText(2, QCoreApplication.translate("ControlForm", u"IMU 3", None))

        self.label_9.setText(QCoreApplication.translate("ControlForm", u"Step size:", None))
        self.comboControlChannel.setItemText(0, QCoreApplication.translate("ControlForm", u"Output 1", None))
        self.comboControlChannel.setItemText(1, QCoreApplication.translate("ControlForm", u"Output 2", None))
        self.comboControlChannel.setItemText(2, QCoreApplication.translate("ControlForm", u"Output 3", None))
        self.comboControlChannel.setItemText(3, QCoreApplication.translate("ControlForm", u"Output 4", None))

        self.comboControlChannel.setCurrentText(QCoreApplication.translate("ControlForm", u"Output 1", None))
        self.comboRef.setItemText(0, QCoreApplication.translate("ControlForm", u"X-Axis Accelerometer", None))
        self.comboRef.setItemText(1, QCoreApplication.translate("ControlForm", u"Y-Axis Accelerometer", None))
        self.comboRef.setItemText(2, QCoreApplication.translate("ControlForm", u"Z-Axis Accelerometer", None))
        self.comboRef.setItemText(3, QCoreApplication.translate("ControlForm", u"X-Axis Gyro", None))
        self.comboRef.setItemText(4, QCoreApplication.translate("ControlForm", u"Y-Axis Gyro", None))
        self.comboRef.setItemText(5, QCoreApplication.translate("ControlForm", u"Z-Axis Gyro", None))

        self.label_12.setText(QCoreApplication.translate("ControlForm", u"Memory size:", None))
        self.comboErro.setItemText(0, QCoreApplication.translate("ControlForm", u"X-Axis Accelerometer", None))
        self.comboErro.setItemText(1, QCoreApplication.translate("ControlForm", u"Y-Axis Accelerometer", None))
        self.comboErro.setItemText(2, QCoreApplication.translate("ControlForm", u"Z-Axis Accelerometer", None))
        self.comboErro.setItemText(3, QCoreApplication.translate("ControlForm", u"X-Axis Gyro", None))
        self.comboErro.setItemText(4, QCoreApplication.translate("ControlForm", u"Y-Axis Gyro", None))
        self.comboErro.setItemText(5, QCoreApplication.translate("ControlForm", u"Z-Axis Gyro", None))

        self.comboAlgoritmo.setItemText(0, QCoreApplication.translate("ControlForm", u"FxNLMS", None))
        self.comboAlgoritmo.setItemText(1, QCoreApplication.translate("ControlForm", u"FxLMS", None))
        self.comboAlgoritmo.setItemText(2, QCoreApplication.translate("ControlForm", u"FxNLMS Modificado Proposto", None))

        self.passoCtrl.setText(QCoreApplication.translate("ControlForm", u"0.01", None))
        self.label_10.setText(QCoreApplication.translate("ControlForm", u"Parameters:", None))
        self.comboPerturbChannel.setItemText(0, QCoreApplication.translate("ControlForm", u"Output 1", None))
        self.comboPerturbChannel.setItemText(1, QCoreApplication.translate("ControlForm", u"Output 2", None))
        self.comboPerturbChannel.setItemText(2, QCoreApplication.translate("ControlForm", u"Output 3", None))
        self.comboPerturbChannel.setItemText(3, QCoreApplication.translate("ControlForm", u"Output 4", None))

    # retranslateUi

