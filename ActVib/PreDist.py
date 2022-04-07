# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PreDist.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_PreDistDialog(object):
    def setupUi(self, PreDistDialog):
        if not PreDistDialog.objectName():
            PreDistDialog.setObjectName(u"PreDistDialog")
        PreDistDialog.resize(518, 255)
        self.gridLayout_2 = QGridLayout(PreDistDialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(3, 3, 3, 3)
        self.label = QLabel(PreDistDialog)
        self.label.setObjectName(u"label")
        self.label.setAutoFillBackground(False)
        self.label.setFrameShape(QFrame.Box)
        self.label.setFrameShadow(QFrame.Raised)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 2)

        self.checkEnable4 = QCheckBox(PreDistDialog)
        self.checkEnable4.setObjectName(u"checkEnable4")

        self.gridLayout_2.addWidget(self.checkEnable4, 4, 0, 1, 1)

        self.checkEnable3 = QCheckBox(PreDistDialog)
        self.checkEnable3.setObjectName(u"checkEnable3")

        self.gridLayout_2.addWidget(self.checkEnable3, 3, 0, 1, 1)

        self.checkEnable2 = QCheckBox(PreDistDialog)
        self.checkEnable2.setObjectName(u"checkEnable2")

        self.gridLayout_2.addWidget(self.checkEnable2, 2, 0, 1, 1)

        self.statusLabel = QLabel(PreDistDialog)
        self.statusLabel.setObjectName(u"statusLabel")

        self.gridLayout_2.addWidget(self.statusLabel, 7, 0, 1, 2)

        self.bSave = QPushButton(PreDistDialog)
        self.bSave.setObjectName(u"bSave")

        self.gridLayout_2.addWidget(self.bSave, 6, 0, 1, 2)

        self.textPoly3 = QLineEdit(PreDistDialog)
        self.textPoly3.setObjectName(u"textPoly3")

        self.gridLayout_2.addWidget(self.textPoly3, 3, 1, 1, 1)

        self.textPoly2 = QLineEdit(PreDistDialog)
        self.textPoly2.setObjectName(u"textPoly2")

        self.gridLayout_2.addWidget(self.textPoly2, 2, 1, 1, 1)

        self.checkEnable1 = QCheckBox(PreDistDialog)
        self.checkEnable1.setObjectName(u"checkEnable1")

        self.gridLayout_2.addWidget(self.checkEnable1, 1, 0, 1, 1)

        self.textPoly1 = QLineEdit(PreDistDialog)
        self.textPoly1.setObjectName(u"textPoly1")

        self.gridLayout_2.addWidget(self.textPoly1, 1, 1, 1, 1)

        self.textPoly4 = QLineEdit(PreDistDialog)
        self.textPoly4.setObjectName(u"textPoly4")

        self.gridLayout_2.addWidget(self.textPoly4, 4, 1, 1, 1)


        self.retranslateUi(PreDistDialog)

        QMetaObject.connectSlotsByName(PreDistDialog)
    # setupUi

    def retranslateUi(self, PreDistDialog):
        PreDistDialog.setWindowTitle(QCoreApplication.translate("PreDistDialog", u"Pre-distortion Configuration", None))
        self.label.setText(QCoreApplication.translate("PreDistDialog", u"<html><head/><body><p align=\"center\"><span style=\" font-size:9pt;\"><br/>Input must be an array containing the polynomial coefficients </span><span style=\" font-size:9pt; font-weight:600;\">[a(k) a(k-1) ... a(0)]</span><span style=\" font-size:9pt;\">,</span></p><p align=\"center\"><span style=\" font-size:9pt;\">where </span><span style=\" font-size:9pt; font-weight:600;\">y = a(k)*x</span><span style=\" font-size:9pt; font-weight:600; vertical-align:super;\">k</span><span style=\" font-size:9pt; font-weight:600;\"> + a(k-1)*x</span><span style=\" font-size:9pt; font-weight:600; vertical-align:super;\">k-1</span><span style=\" font-size:9pt; font-weight:600;\"> + ... + a(1)*x + a(0)</span><span style=\" font-size:9pt;\">. Thus, for a </span><span style=\" font-size:9pt; font-weight:600;\">K-th</span><span style=\" font-size:9pt;\"> order </span></p><p align=\"center\"><span style=\" font-size:9pt;\">polynomial, </span><span style=\" font-size:9pt; font-weight:600;\">K+1</span><span style=\" font-size:9pt;"
                        "\"> coefficients are required. Maximum order is </span><span style=\" font-size:9pt; font-weight:600;\">9</span><span style=\" font-size:9pt;\">.<br/></span></p></body></html>", None))
        self.checkEnable4.setText(QCoreApplication.translate("PreDistDialog", u"Enable for Output 4:", None))
        self.checkEnable3.setText(QCoreApplication.translate("PreDistDialog", u"Enable for Output 3:", None))
        self.checkEnable2.setText(QCoreApplication.translate("PreDistDialog", u"Enable for Output 2:", None))
        self.statusLabel.setText("")
        self.bSave.setText(QCoreApplication.translate("PreDistDialog", u"Check and Save", None))
        self.textPoly3.setText(QCoreApplication.translate("PreDistDialog", u"[0.0  0.0  0.0  0.0  0.0  0.0  0.0]", None))
        self.textPoly2.setText(QCoreApplication.translate("PreDistDialog", u"[0.0  0.0  0.0  0.0  0.0  0.0  0.0]", None))
        self.checkEnable1.setText(QCoreApplication.translate("PreDistDialog", u"Enable for Output 1:", None))
        self.textPoly1.setText(QCoreApplication.translate("PreDistDialog", u"[0.0  0.0  0.0  0.0  0.0  0.0  0.0]", None))
        self.textPoly4.setText(QCoreApplication.translate("PreDistDialog", u"[0.0  0.0  0.0  0.0  0.0  0.0  0.0]", None))
    # retranslateUi

