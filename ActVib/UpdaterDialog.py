# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'UpdaterDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QPushButton,
    QSizePolicy, QTextEdit, QWidget)

class Ui_UpdaterDialog(object):
    def setupUi(self, UpdaterDialog):
        if not UpdaterDialog.objectName():
            UpdaterDialog.setObjectName(u"UpdaterDialog")
        UpdaterDialog.resize(612, 435)
        self.gridLayout = QGridLayout(UpdaterDialog)
        self.gridLayout.setSpacing(3)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(3, 3, 3, 3)
        self.startFirmware = QPushButton(UpdaterDialog)
        self.startFirmware.setObjectName(u"startFirmware")

        self.gridLayout.addWidget(self.startFirmware, 1, 0, 1, 1)

        self.startSoftware = QPushButton(UpdaterDialog)
        self.startSoftware.setObjectName(u"startSoftware")
        self.startSoftware.setEnabled(True)

        self.gridLayout.addWidget(self.startSoftware, 1, 1, 1, 1)

        self.messageArea = QTextEdit(UpdaterDialog)
        self.messageArea.setObjectName(u"messageArea")

        self.gridLayout.addWidget(self.messageArea, 0, 0, 1, 2)


        self.retranslateUi(UpdaterDialog)

        QMetaObject.connectSlotsByName(UpdaterDialog)
    # setupUi

    def retranslateUi(self, UpdaterDialog):
        UpdaterDialog.setWindowTitle(QCoreApplication.translate("UpdaterDialog", u"Firmware/Software Updater", None))
        self.startFirmware.setText(QCoreApplication.translate("UpdaterDialog", u"Start Firmware Update...", None))
        self.startSoftware.setText(QCoreApplication.translate("UpdaterDialog", u"Start Software Update...", None))
    # retranslateUi

