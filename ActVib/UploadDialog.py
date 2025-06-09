# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'UploadDialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QFrame, QGridLayout, QLabel,
    QLineEdit, QProgressBar, QPushButton, QSizePolicy,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(450, 216)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(300, 0))
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.status = QLabel(Dialog)
        self.status.setObjectName(u"status")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.status.sizePolicy().hasHeightForWidth())
        self.status.setSizePolicy(sizePolicy1)
        self.status.setMinimumSize(QSize(0, 20))
        self.status.setFrameShape(QFrame.StyledPanel)

        self.gridLayout.addWidget(self.status, 6, 0, 1, 3)

        self.bAbre = QPushButton(Dialog)
        self.bAbre.setObjectName(u"bAbre")

        self.gridLayout.addWidget(self.bAbre, 1, 2, 1, 1)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Close)

        self.gridLayout.addWidget(self.buttonBox, 7, 0, 1, 3)

        self.bGravar = QPushButton(Dialog)
        self.bGravar.setObjectName(u"bGravar")

        self.gridLayout.addWidget(self.bGravar, 4, 0, 1, 3)

        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.progressBar = QProgressBar(Dialog)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(24)
        self.progressBar.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.progressBar, 3, 0, 1, 3)

        self.caminhoArquivo = QLineEdit(Dialog)
        self.caminhoArquivo.setObjectName(u"caminhoArquivo")

        self.gridLayout.addWidget(self.caminhoArquivo, 1, 1, 1, 1)

        self.comboTipo = QComboBox(Dialog)
        self.comboTipo.addItem("")
        self.comboTipo.addItem("")
        self.comboTipo.addItem("")
        self.comboTipo.addItem("")
        self.comboTipo.setObjectName(u"comboTipo")

        self.gridLayout.addWidget(self.comboTipo, 0, 0, 1, 3)

        self.bGravaFlash = QPushButton(Dialog)
        self.bGravaFlash.setObjectName(u"bGravaFlash")

        self.gridLayout.addWidget(self.bGravaFlash, 5, 0, 1, 3)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Path Upload", None))
        self.status.setText("")
        self.bAbre.setText(QCoreApplication.translate("Dialog", u"...", None))
        self.bGravar.setText(QCoreApplication.translate("Dialog", u"Upload data...", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Choose file:", None))
        self.comboTipo.setItemText(0, QCoreApplication.translate("Dialog", u"Both Secondary and Feedback Paths (from File)", None))
        self.comboTipo.setItemText(1, QCoreApplication.translate("Dialog", u"Both Secondary and Feedback Paths (from Memory)", None))
        self.comboTipo.setItemText(2, QCoreApplication.translate("Dialog", u"Secondary Path (from File)", None))
        self.comboTipo.setItemText(3, QCoreApplication.translate("Dialog", u"Feedback Path  (from File)", None))

        self.bGravaFlash.setText(QCoreApplication.translate("Dialog", u"Record in Flash", None))
    # retranslateUi

