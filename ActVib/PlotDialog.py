# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PlotDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(200, 160)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout.setContentsMargins(9, 3, 9, 3)
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.janelaX = QtWidgets.QSpinBox(self.groupBox_2)
        self.janelaX.setMinimum(1)
        self.janelaX.setMaximum(600)
        self.janelaX.setSingleStep(10)
        self.janelaX.setProperty("value", 30)
        self.janelaX.setObjectName("janelaX")
        self.horizontalLayout.addWidget(self.janelaX)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setContentsMargins(9, 3, -1, 3)
        self.gridLayout_2.setSpacing(3)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)
        self.minY = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.minY.setMinimum(-2000.0)
        self.minY.setMaximum(2000.0)
        self.minY.setProperty("value", -100.0)
        self.minY.setObjectName("minY")
        self.gridLayout_2.addWidget(self.minY, 3, 1, 1, 1)
        self.maxY = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.maxY.setMinimum(-2000.0)
        self.maxY.setMaximum(2000.0)
        self.maxY.setProperty("value", 100.0)
        self.maxY.setObjectName("maxY")
        self.gridLayout_2.addWidget(self.maxY, 2, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 3, 0, 1, 1)
        self.checkAutoY = QtWidgets.QCheckBox(self.groupBox)
        self.checkAutoY.setObjectName("checkAutoY")
        self.gridLayout_2.addWidget(self.checkAutoY, 1, 0, 1, 2)
        self.verticalLayout.addWidget(self.groupBox)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Plot Config"))
        self.groupBox_2.setTitle(_translate("Dialog", " Eixo X "))
        self.label.setText(_translate("Dialog", "Janela de Tempo:"))
        self.janelaX.setSuffix(_translate("Dialog", " s"))
        self.groupBox.setTitle(_translate("Dialog", " Eixo Y "))
        self.label_2.setText(_translate("Dialog", "Máximo em Y:"))
        self.label_3.setText(_translate("Dialog", "Mínimo em Y:"))
        self.checkAutoY.setText(_translate("Dialog", "Auto"))
