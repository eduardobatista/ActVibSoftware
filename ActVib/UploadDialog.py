# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UploadDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(450, 207)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(300, 0))
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.status = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.status.sizePolicy().hasHeightForWidth())
        self.status.setSizePolicy(sizePolicy)
        self.status.setMinimumSize(QtCore.QSize(0, 20))
        self.status.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.status.setText("")
        self.status.setObjectName("status")
        self.gridLayout.addWidget(self.status, 6, 0, 1, 3)
        self.bAbre = QtWidgets.QPushButton(Dialog)
        self.bAbre.setObjectName("bAbre")
        self.gridLayout.addWidget(self.bAbre, 1, 2, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 7, 0, 1, 3)
        self.bGravar = QtWidgets.QPushButton(Dialog)
        self.bGravar.setObjectName("bGravar")
        self.gridLayout.addWidget(self.bGravar, 4, 0, 1, 3)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(Dialog)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 3, 0, 1, 3)
        self.caminhoArquivo = QtWidgets.QLineEdit(Dialog)
        self.caminhoArquivo.setObjectName("caminhoArquivo")
        self.gridLayout.addWidget(self.caminhoArquivo, 1, 1, 1, 1)
        self.comboTipo = QtWidgets.QComboBox(Dialog)
        self.comboTipo.setObjectName("comboTipo")
        self.comboTipo.addItem("")
        self.comboTipo.addItem("")
        self.comboTipo.addItem("")
        self.gridLayout.addWidget(self.comboTipo, 0, 0, 1, 3)
        self.bGravaFlash = QtWidgets.QPushButton(Dialog)
        self.bGravaFlash.setObjectName("bGravaFlash")
        self.gridLayout.addWidget(self.bGravaFlash, 5, 0, 1, 3)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.bAbre.setText(_translate("Dialog", "..."))
        self.bGravar.setText(_translate("Dialog", "Fazer Upload ..."))
        self.label.setText(_translate("Dialog", "Escolhar o arquivo:"))
        self.comboTipo.setItemText(0, _translate("Dialog", "Ambos"))
        self.comboTipo.setItemText(1, _translate("Dialog", "Caminho Secundário"))
        self.comboTipo.setItemText(2, _translate("Dialog", "Caminho de FeedBack"))
        self.bGravaFlash.setText(_translate("Dialog", "Gravar em Definitivo na Flash"))
