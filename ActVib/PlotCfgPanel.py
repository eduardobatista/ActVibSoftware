# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PlotCfgPanel.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_PlotCfgForm(object):
    def setupUi(self, PlotCfgForm):
        if not PlotCfgForm.objectName():
            PlotCfgForm.setObjectName(u"PlotCfgForm")
        PlotCfgForm.resize(426, 52)
        self.verticalLayout_2 = QVBoxLayout(PlotCfgForm)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.plotcfgframe = QFrame(PlotCfgForm)
        self.plotcfgframe.setObjectName(u"plotcfgframe")
        self.plotcfgframe.setFrameShape(QFrame.NoFrame)
        self.plotcfgframe.setFrameShadow(QFrame.Plain)
        self.plotcfgframe.setLineWidth(0)
        self.horizontalLayout_2 = QHBoxLayout(self.plotcfgframe)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 2, 0, 2)
        self.label_31 = QLabel(self.plotcfgframe)
        self.label_31.setObjectName(u"label_31")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_31.sizePolicy().hasHeightForWidth())
        self.label_31.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.label_31)

        self.comboPlot1 = QComboBox(self.plotcfgframe)
        self.comboPlot1.addItem("")
        self.comboPlot1.addItem("")
        self.comboPlot1.addItem("")
        self.comboPlot1.setObjectName(u"comboPlot1")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.comboPlot1.sizePolicy().hasHeightForWidth())
        self.comboPlot1.setSizePolicy(sizePolicy1)

        self.horizontalLayout_2.addWidget(self.comboPlot1)

        self.label_32 = QLabel(self.plotcfgframe)
        self.label_32.setObjectName(u"label_32")
        sizePolicy.setHeightForWidth(self.label_32.sizePolicy().hasHeightForWidth())
        self.label_32.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.label_32)

        self.comboPlot2 = QComboBox(self.plotcfgframe)
        self.comboPlot2.addItem("")
        self.comboPlot2.addItem("")
        self.comboPlot2.addItem("")
        self.comboPlot2.setObjectName(u"comboPlot2")
        sizePolicy1.setHeightForWidth(self.comboPlot2.sizePolicy().hasHeightForWidth())
        self.comboPlot2.setSizePolicy(sizePolicy1)

        self.horizontalLayout_2.addWidget(self.comboPlot2)


        self.verticalLayout_2.addWidget(self.plotcfgframe)

        self.frame = QFrame(PlotCfgForm)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Plain)
        self.frame.setLineWidth(0)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 2, 0, 2)
        self.checkAccX = QCheckBox(self.frame)
        self.checkAccX.setObjectName(u"checkAccX")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.checkAccX.sizePolicy().hasHeightForWidth())
        self.checkAccX.setSizePolicy(sizePolicy2)
        self.checkAccX.setChecked(True)

        self.horizontalLayout.addWidget(self.checkAccX)

        self.checkAccY = QCheckBox(self.frame)
        self.checkAccY.setObjectName(u"checkAccY")
        sizePolicy2.setHeightForWidth(self.checkAccY.sizePolicy().hasHeightForWidth())
        self.checkAccY.setSizePolicy(sizePolicy2)
        self.checkAccY.setChecked(True)

        self.horizontalLayout.addWidget(self.checkAccY)

        self.checkAccZ = QCheckBox(self.frame)
        self.checkAccZ.setObjectName(u"checkAccZ")
        sizePolicy2.setHeightForWidth(self.checkAccZ.sizePolicy().hasHeightForWidth())
        self.checkAccZ.setSizePolicy(sizePolicy2)
        self.checkAccZ.setChecked(True)

        self.horizontalLayout.addWidget(self.checkAccZ)

        self.checkGyroX = QCheckBox(self.frame)
        self.checkGyroX.setObjectName(u"checkGyroX")
        sizePolicy2.setHeightForWidth(self.checkGyroX.sizePolicy().hasHeightForWidth())
        self.checkGyroX.setSizePolicy(sizePolicy2)
        self.checkGyroX.setChecked(True)

        self.horizontalLayout.addWidget(self.checkGyroX)

        self.checkGyroY = QCheckBox(self.frame)
        self.checkGyroY.setObjectName(u"checkGyroY")
        sizePolicy2.setHeightForWidth(self.checkGyroY.sizePolicy().hasHeightForWidth())
        self.checkGyroY.setSizePolicy(sizePolicy2)
        self.checkGyroY.setChecked(True)

        self.horizontalLayout.addWidget(self.checkGyroY)

        self.checkGyroZ = QCheckBox(self.frame)
        self.checkGyroZ.setObjectName(u"checkGyroZ")
        sizePolicy2.setHeightForWidth(self.checkGyroZ.sizePolicy().hasHeightForWidth())
        self.checkGyroZ.setSizePolicy(sizePolicy2)
        self.checkGyroZ.setChecked(True)

        self.horizontalLayout.addWidget(self.checkGyroZ)


        self.verticalLayout_2.addWidget(self.frame)


        self.retranslateUi(PlotCfgForm)

        self.comboPlot2.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(PlotCfgForm)
    # setupUi

    def retranslateUi(self, PlotCfgForm):
        PlotCfgForm.setWindowTitle(QCoreApplication.translate("PlotCfgForm", u"Form", None))
        self.label_31.setText(QCoreApplication.translate("PlotCfgForm", u"Plot 1:", None))
        self.comboPlot1.setItemText(0, QCoreApplication.translate("PlotCfgForm", u"IMU 1: Acceleration", None))
        self.comboPlot1.setItemText(1, QCoreApplication.translate("PlotCfgForm", u"IMU 2: Acceleration", None))
        self.comboPlot1.setItemText(2, QCoreApplication.translate("PlotCfgForm", u"IMU 3: Acceleration", None))

        self.label_32.setText(QCoreApplication.translate("PlotCfgForm", u"Plot 2:", None))
        self.comboPlot2.setItemText(0, QCoreApplication.translate("PlotCfgForm", u"IMU 1: Gyro", None))
        self.comboPlot2.setItemText(1, QCoreApplication.translate("PlotCfgForm", u"IMU 2: Gyro", None))
        self.comboPlot2.setItemText(2, QCoreApplication.translate("PlotCfgForm", u"IMU 3: Gyro", None))

        self.comboPlot2.setCurrentText(QCoreApplication.translate("PlotCfgForm", u"IMU 1: Gyro", None))
        self.checkAccX.setText(QCoreApplication.translate("PlotCfgForm", u"AccX", None))
        self.checkAccY.setText(QCoreApplication.translate("PlotCfgForm", u"AccY", None))
        self.checkAccZ.setText(QCoreApplication.translate("PlotCfgForm", u"AccZ", None))
        self.checkGyroX.setText(QCoreApplication.translate("PlotCfgForm", u"GyroX", None))
        self.checkGyroY.setText(QCoreApplication.translate("PlotCfgForm", u"GyroY", None))
        self.checkGyroZ.setText(QCoreApplication.translate("PlotCfgForm", u"GyroZ", None))
    # retranslateUi

