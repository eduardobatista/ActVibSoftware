# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'VibViewWindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1090, 732)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.actionSalvar_dados = QAction(MainWindow)
        self.actionSalvar_dados.setObjectName(u"actionSalvar_dados")
        self.actionSair = QAction(MainWindow)
        self.actionSair.setObjectName(u"actionSair")
        self.actionCOM1 = QAction(MainWindow)
        self.actionCOM1.setObjectName(u"actionCOM1")
        self.actionCOM2 = QAction(MainWindow)
        self.actionCOM2.setObjectName(u"actionCOM2")
        self.actionCOM3 = QAction(MainWindow)
        self.actionCOM3.setObjectName(u"actionCOM3")
        self.actionCOM4 = QAction(MainWindow)
        self.actionCOM4.setObjectName(u"actionCOM4")
        self.actionCOM5 = QAction(MainWindow)
        self.actionCOM5.setObjectName(u"actionCOM5")
        self.actionCOM6 = QAction(MainWindow)
        self.actionCOM6.setObjectName(u"actionCOM6")
        self.actionCOM7 = QAction(MainWindow)
        self.actionCOM7.setObjectName(u"actionCOM7")
        self.actionCOM8 = QAction(MainWindow)
        self.actionCOM8.setObjectName(u"actionCOM8")
        self.actionCOM9 = QAction(MainWindow)
        self.actionCOM9.setObjectName(u"actionCOM9")
        self.actionCOM10 = QAction(MainWindow)
        self.actionCOM10.setObjectName(u"actionCOM10")
        self.actionCOM11 = QAction(MainWindow)
        self.actionCOM11.setObjectName(u"actionCOM11")
        self.actionCOM12 = QAction(MainWindow)
        self.actionCOM12.setObjectName(u"actionCOM12")
        self.actionUpload = QAction(MainWindow)
        self.actionUpload.setObjectName(u"actionUpload")
        self.actionDefineWorkdir = QAction(MainWindow)
        self.actionDefineWorkdir.setObjectName(u"actionDefineWorkdir")
        self.actionSavePlus = QAction(MainWindow)
        self.actionSavePlus.setObjectName(u"actionSavePlus")
        self.actionWorkdirManager = QAction(MainWindow)
        self.actionWorkdirManager.setObjectName(u"actionWorkdirManager")
        self.actionTeste = QAction(MainWindow)
        self.actionTeste.setObjectName(u"actionTeste")
        self.action1_ms = QAction(MainWindow)
        self.action1_ms.setObjectName(u"action1_ms")
        self.action2_ms = QAction(MainWindow)
        self.action2_ms.setObjectName(u"action2_ms")
        self.action3_ms = QAction(MainWindow)
        self.action3_ms.setObjectName(u"action3_ms")
        self.action4_ms = QAction(MainWindow)
        self.action4_ms.setObjectName(u"action4_ms")
        self.action5_ms = QAction(MainWindow)
        self.action5_ms.setObjectName(u"action5_ms")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame_3 = QFrame(self.centralwidget)
        self.frame_3.setObjectName(u"frame_3")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy1)
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.frame_3.setLineWidth(0)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.label_4 = QLabel(self.frame_3)
        self.label_4.setObjectName(u"label_4")
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)

        self.horizontalLayout_3.addWidget(self.label_4)

        self.elapsedTime = QLabel(self.frame_3)
        self.elapsedTime.setObjectName(u"elapsedTime")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.elapsedTime.sizePolicy().hasHeightForWidth())
        self.elapsedTime.setSizePolicy(sizePolicy2)
        self.elapsedTime.setMinimumSize(QSize(200, 0))
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(True)
        font1.setWeight(75)
        self.elapsedTime.setFont(font1)
        self.elapsedTime.setFrameShape(QFrame.StyledPanel)
        self.elapsedTime.setLineWidth(2)
        self.elapsedTime.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.elapsedTime)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.label_5 = QLabel(self.frame_3)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)

        self.horizontalLayout_3.addWidget(self.label_5)

        self.controlTime = QLabel(self.frame_3)
        self.controlTime.setObjectName(u"controlTime")
        sizePolicy2.setHeightForWidth(self.controlTime.sizePolicy().hasHeightForWidth())
        self.controlTime.setSizePolicy(sizePolicy2)
        self.controlTime.setMinimumSize(QSize(200, 0))
        self.controlTime.setFont(font1)
        self.controlTime.setFrameShape(QFrame.StyledPanel)
        self.controlTime.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.controlTime)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.label_6 = QLabel(self.frame_3)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font)

        self.horizontalLayout_3.addWidget(self.label_6)

        self.sampleTime = QLabel(self.frame_3)
        self.sampleTime.setObjectName(u"sampleTime")
        sizePolicy2.setHeightForWidth(self.sampleTime.sizePolicy().hasHeightForWidth())
        self.sampleTime.setSizePolicy(sizePolicy2)
        self.sampleTime.setMinimumSize(QSize(200, 0))
        self.sampleTime.setFont(font1)
        self.sampleTime.setFrameShape(QFrame.StyledPanel)
        self.sampleTime.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.sampleTime)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addWidget(self.frame_3)

        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setLineWidth(0)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(3, 0, 3, 0)
        self.frame11 = QFrame(self.frame)
        self.frame11.setObjectName(u"frame11")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.frame11.sizePolicy().hasHeightForWidth())
        self.frame11.setSizePolicy(sizePolicy3)
        self.verticalLayout_2 = QVBoxLayout(self.frame11)
        self.verticalLayout_2.setSpacing(3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(3, 3, 3, 3)
        self.tabWidget = QTabWidget(self.frame11)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy1)
        self.tabWidget.setBaseSize(QSize(0, 0))
        self.tabWidget.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.tabWidget.setElideMode(Qt.ElideLeft)
        self.tabWidget.setTabBarAutoHide(False)
        self.canal1 = QWidget()
        self.canal1.setObjectName(u"canal1")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.canal1.sizePolicy().hasHeightForWidth())
        self.canal1.setSizePolicy(sizePolicy4)
        self.canal1.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.verticalLayout_7 = QVBoxLayout(self.canal1)
        self.verticalLayout_7.setSpacing(3)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(3, 3, 3, 3)
        self.tabWidget.addTab(self.canal1, "")
        self.canal2 = QWidget()
        self.canal2.setObjectName(u"canal2")
        sizePolicy4.setHeightForWidth(self.canal2.sizePolicy().hasHeightForWidth())
        self.canal2.setSizePolicy(sizePolicy4)
        self.verticalLayout_6 = QVBoxLayout(self.canal2)
        self.verticalLayout_6.setSpacing(3)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(3, 3, 3, 3)
        self.tabWidget.addTab(self.canal2, "")
        self.canal3 = QWidget()
        self.canal3.setObjectName(u"canal3")
        sizePolicy4.setHeightForWidth(self.canal3.sizePolicy().hasHeightForWidth())
        self.canal3.setSizePolicy(sizePolicy4)
        self.verticalLayout_4 = QVBoxLayout(self.canal3)
        self.verticalLayout_4.setSpacing(3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(3, 3, 3, 3)
        self.tabWidget.addTab(self.canal3, "")
        self.canal4 = QWidget()
        self.canal4.setObjectName(u"canal4")
        sizePolicy4.setHeightForWidth(self.canal4.sizePolicy().hasHeightForWidth())
        self.canal4.setSizePolicy(sizePolicy4)
        self.verticalLayout_5 = QVBoxLayout(self.canal4)
        self.verticalLayout_5.setSpacing(3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(3, 3, 3, 3)
        self.tabWidget.addTab(self.canal4, "")

        self.verticalLayout_2.addWidget(self.tabWidget)

        self.controlFrame = QFrame(self.frame11)
        self.controlFrame.setObjectName(u"controlFrame")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.controlFrame.sizePolicy().hasHeightForWidth())
        self.controlFrame.setSizePolicy(sizePolicy5)
        self.controlFrame.setMinimumSize(QSize(0, 20))
        self.controlFrame.setAutoFillBackground(False)
        self.controlFrame.setStyleSheet(u"")
        self.controlFrame.setFrameShape(QFrame.Box)
        self.controlFrame.setFrameShadow(QFrame.Sunken)
        self.horizontalLayout_5 = QHBoxLayout(self.controlFrame)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_2.addWidget(self.controlFrame)

        self.frame_5 = QFrame(self.frame11)
        self.frame_5.setObjectName(u"frame_5")
        sizePolicy6 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.frame_5.sizePolicy().hasHeightForWidth())
        self.frame_5.setSizePolicy(sizePolicy6)
        self.frame_5.setMinimumSize(QSize(10, 10))
        self.frame_5.setMaximumSize(QSize(1000, 1000))
        self.frame_5.setBaseSize(QSize(25, 25))
        self.frame_5.setAutoFillBackground(False)
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.plotLayout2 = QVBoxLayout(self.frame_5)
        self.plotLayout2.setSpacing(0)
        self.plotLayout2.setObjectName(u"plotLayout2")
        self.plotLayout2.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_2.addWidget(self.frame_5)


        self.horizontalLayout.addWidget(self.frame11)

        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy3.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy3)
        self.verticalLayout_3 = QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setSpacing(3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(3, 3, 3, 3)
        self.tabSensors = QTabWidget(self.frame_2)
        self.tabSensors.setObjectName(u"tabSensors")
        sizePolicy7 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.tabSensors.sizePolicy().hasHeightForWidth())
        self.tabSensors.setSizePolicy(sizePolicy7)
        self.imutab1 = QWidget()
        self.imutab1.setObjectName(u"imutab1")
        self.IMU1Layout = QVBoxLayout(self.imutab1)
        self.IMU1Layout.setObjectName(u"IMU1Layout")
        self.IMU1Layout.setContentsMargins(8, 3, 8, 3)
        self.tabSensors.addTab(self.imutab1, "")
        self.imutab2 = QWidget()
        self.imutab2.setObjectName(u"imutab2")
        self.verticalLayout_9 = QVBoxLayout(self.imutab2)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.tabSensors.addTab(self.imutab2, "")
        self.imutab3 = QWidget()
        self.imutab3.setObjectName(u"imutab3")
        self.verticalLayout_10 = QVBoxLayout(self.imutab3)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.tabSensors.addTab(self.imutab3, "")
        self.adctab = QWidget()
        self.adctab.setObjectName(u"adctab")
        self.verticalLayout_13 = QVBoxLayout(self.adctab)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(8, 3, 8, 3)
        self.tabSensors.addTab(self.adctab, "")

        self.verticalLayout_3.addWidget(self.tabSensors)

        self.plotCfgFrame = QFrame(self.frame_2)
        self.plotCfgFrame.setObjectName(u"plotCfgFrame")
        sizePolicy4.setHeightForWidth(self.plotCfgFrame.sizePolicy().hasHeightForWidth())
        self.plotCfgFrame.setSizePolicy(sizePolicy4)
        self.plotCfgFrame.setFrameShape(QFrame.Box)
        self.plotCfgFrame.setFrameShadow(QFrame.Sunken)
        self.horizontalLayout_13 = QHBoxLayout(self.plotCfgFrame)
        self.horizontalLayout_13.setSpacing(5)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(10, 3, 10, 4)

        self.verticalLayout_3.addWidget(self.plotCfgFrame)

        self.plotFrameOut = QFrame(self.frame_2)
        self.plotFrameOut.setObjectName(u"plotFrameOut")
        sizePolicy6.setHeightForWidth(self.plotFrameOut.sizePolicy().hasHeightForWidth())
        self.plotFrameOut.setSizePolicy(sizePolicy6)
        self.plotFrameOut.setFrameShape(QFrame.StyledPanel)
        self.plotFrameOut.setFrameShadow(QFrame.Raised)
        self.plotOutLayout = QVBoxLayout(self.plotFrameOut)
        self.plotOutLayout.setSpacing(3)
        self.plotOutLayout.setObjectName(u"plotOutLayout")
        self.plotOutLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.plotOutLayout.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_3.addWidget(self.plotFrameOut)


        self.horizontalLayout.addWidget(self.frame_2)


        self.verticalLayout.addWidget(self.frame)

        self.bInit = QPushButton(self.centralwidget)
        self.bInit.setObjectName(u"bInit")
        sizePolicy8 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.bInit.sizePolicy().hasHeightForWidth())
        self.bInit.setSizePolicy(sizePolicy8)

        self.verticalLayout.addWidget(self.bInit)

        self.bLimpar = QPushButton(self.centralwidget)
        self.bLimpar.setObjectName(u"bLimpar")
        sizePolicy8.setHeightForWidth(self.bLimpar.sizePolicy().hasHeightForWidth())
        self.bLimpar.setSizePolicy(sizePolicy8)

        self.verticalLayout.addWidget(self.bLimpar)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1090, 21))
        self.menuArquivo = QMenu(self.menubar)
        self.menuArquivo.setObjectName(u"menuArquivo")
        self.menuArquivo.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.menuSelecionar_Porta = QMenu(self.menuArquivo)
        self.menuSelecionar_Porta.setObjectName(u"menuSelecionar_Porta")
        self.menuSampling_Rate = QMenu(self.menuArquivo)
        self.menuSampling_Rate.setObjectName(u"menuSampling_Rate")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuArquivo.menuAction())
        self.menuArquivo.addAction(self.actionSalvar_dados)
        self.menuArquivo.addAction(self.actionUpload)
        self.menuArquivo.addAction(self.menuSelecionar_Porta.menuAction())
        self.menuArquivo.addAction(self.menuSampling_Rate.menuAction())
        self.menuArquivo.addSeparator()
        self.menuArquivo.addAction(self.actionSavePlus)
        self.menuArquivo.addAction(self.actionDefineWorkdir)
        self.menuArquivo.addAction(self.actionWorkdirManager)
        self.menuArquivo.addSeparator()
        self.menuArquivo.addAction(self.actionSair)
        self.menuSelecionar_Porta.addAction(self.actionCOM1)
        self.menuSelecionar_Porta.addAction(self.actionCOM2)
        self.menuSelecionar_Porta.addAction(self.actionCOM3)
        self.menuSelecionar_Porta.addAction(self.actionCOM4)
        self.menuSelecionar_Porta.addAction(self.actionCOM5)
        self.menuSelecionar_Porta.addAction(self.actionCOM6)
        self.menuSelecionar_Porta.addAction(self.actionCOM7)
        self.menuSelecionar_Porta.addAction(self.actionCOM8)
        self.menuSelecionar_Porta.addAction(self.actionCOM9)
        self.menuSelecionar_Porta.addAction(self.actionCOM10)
        self.menuSelecionar_Porta.addAction(self.actionCOM11)
        self.menuSelecionar_Porta.addAction(self.actionCOM12)
        self.menuSampling_Rate.addAction(self.action1_ms)
        self.menuSampling_Rate.addAction(self.action2_ms)
        self.menuSampling_Rate.addAction(self.action3_ms)
        self.menuSampling_Rate.addAction(self.action4_ms)
        self.menuSampling_Rate.addAction(self.action5_ms)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)
        self.tabSensors.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"ActVib", None))
        self.actionSalvar_dados.setText(QCoreApplication.translate("MainWindow", u"Save...", None))
        self.actionSair.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
        self.actionCOM1.setText(QCoreApplication.translate("MainWindow", u"COM1", None))
        self.actionCOM2.setText(QCoreApplication.translate("MainWindow", u"COM2", None))
        self.actionCOM3.setText(QCoreApplication.translate("MainWindow", u"COM3", None))
        self.actionCOM4.setText(QCoreApplication.translate("MainWindow", u"COM4", None))
        self.actionCOM5.setText(QCoreApplication.translate("MainWindow", u"COM5", None))
        self.actionCOM6.setText(QCoreApplication.translate("MainWindow", u"COM6", None))
        self.actionCOM7.setText(QCoreApplication.translate("MainWindow", u"COM7", None))
        self.actionCOM8.setText(QCoreApplication.translate("MainWindow", u"COM8", None))
        self.actionCOM9.setText(QCoreApplication.translate("MainWindow", u"COM9", None))
        self.actionCOM10.setText(QCoreApplication.translate("MainWindow", u"COM10", None))
        self.actionCOM11.setText(QCoreApplication.translate("MainWindow", u"COM11", None))
        self.actionCOM12.setText(QCoreApplication.translate("MainWindow", u"COM12", None))
        self.actionUpload.setText(QCoreApplication.translate("MainWindow", u"Upload secondary and feedback responses...", None))
        self.actionDefineWorkdir.setText(QCoreApplication.translate("MainWindow", u"Define Workdir", None))
        self.actionSavePlus.setText(QCoreApplication.translate("MainWindow", u"Save and Update Metada in Workdir", None))
        self.actionWorkdirManager.setText(QCoreApplication.translate("MainWindow", u"Workdir Manager", None))
        self.actionTeste.setText(QCoreApplication.translate("MainWindow", u"Teste", None))
        self.action1_ms.setText(QCoreApplication.translate("MainWindow", u"1 ms", None))
        self.action2_ms.setText(QCoreApplication.translate("MainWindow", u"2 ms", None))
        self.action3_ms.setText(QCoreApplication.translate("MainWindow", u"3 ms", None))
        self.action4_ms.setText(QCoreApplication.translate("MainWindow", u"4 ms", None))
        self.action5_ms.setText(QCoreApplication.translate("MainWindow", u"5 ms", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Elapsed Time:", None))
        self.elapsedTime.setText(QCoreApplication.translate("MainWindow", u" 0 s", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Time Delay:", None))
        self.controlTime.setText(QCoreApplication.translate("MainWindow", u"0 s", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Sample Time:", None))
        self.sampleTime.setText(QCoreApplication.translate("MainWindow", u"0 us", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.canal1), QCoreApplication.translate("MainWindow", u"Output 1", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.canal2), QCoreApplication.translate("MainWindow", u"Output 2", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.canal3), QCoreApplication.translate("MainWindow", u"Output 3", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.canal4), QCoreApplication.translate("MainWindow", u"Output 4", None))
        self.tabSensors.setTabText(self.tabSensors.indexOf(self.imutab1), QCoreApplication.translate("MainWindow", u"IMU 1", None))
        self.tabSensors.setTabText(self.tabSensors.indexOf(self.imutab2), QCoreApplication.translate("MainWindow", u"IMU 2", None))
        self.tabSensors.setTabText(self.tabSensors.indexOf(self.imutab3), QCoreApplication.translate("MainWindow", u"IMU 3", None))
        self.tabSensors.setTabText(self.tabSensors.indexOf(self.adctab), QCoreApplication.translate("MainWindow", u"ADC", None))
        self.bInit.setText(QCoreApplication.translate("MainWindow", u"Start/Stop", None))
        self.bLimpar.setText(QCoreApplication.translate("MainWindow", u"Reset Data", None))
        self.menuArquivo.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuSelecionar_Porta.setTitle(QCoreApplication.translate("MainWindow", u"Port", None))
        self.menuSampling_Rate.setTitle(QCoreApplication.translate("MainWindow", u"Sampling Rate", None))
    # retranslateUi

