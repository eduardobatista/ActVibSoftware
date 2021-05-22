from pathlib import Path
from os import getenv
import time

import pandas as pd

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QCheckBox, QComboBox, QDoubleSpinBox, QSpinBox

from VibViewWindow import Ui_MainWindow

from others import (MyFigQtGraph, CtrlFigQtGraph, FigOutputQtGraph, WorkdirManager, MyUploadDialog)

from panels import (IMUPanel,GeneratorPanel,PlotCfgPanel)

class mainwindow(QtWidgets.QMainWindow):

    def __init__(self, app):
        super(mainwindow, self).__init__()
        self.app = app
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.cw = self.ui.centralwidget
        self.porta = "COM3"
        self.workdir = "D://"
        self.saveconfigtypes = [QtWidgets.QCheckBox, QtWidgets.QComboBox,
                                QtWidgets.QDoubleSpinBox, QtWidgets.QSpinBox, QtWidgets.QLineEdit]
        self.imupanel = [IMUPanel(idd) for idd in range(3)]
        self.genpanel = [GeneratorPanel(1),GeneratorPanel(2),GeneratorPanel(3),GeneratorPanel(4)]
        self.plotcfgpanel = PlotCfgPanel()
        self.readConfig()
        self.mapper = QtCore.QSignalMapper(self)
        self.ui.bInit.clicked.connect(self.bInit)
        self.ui.bLimpar.clicked.connect(self.bReset)
        for acc in self.ui.menuSelecionar_Porta.actions():
            self.mapper.setMapping(acc, acc.text())
            acc.triggered.connect(self.mapper.map)
        self.mapper.mapped['QString'].connect(self.setaPorta)
        self.ui.actionSair.triggered.connect(self.closeEvent)
        self.ui.actionSalvar_dados.triggered.connect(self.saveDialog)
        self.ui.actionUpload.triggered.connect(self.openUploadDialog)
        self.ui.actionWorkdirManager.triggered.connect(self.openWorkdirManager)
        
        # IMU Connections:        
        self.ui.imutab1.layout().addWidget(self.imupanel[0])
        self.ui.imutab2.layout().addWidget(self.imupanel[1])
        self.ui.imutab3.layout().addWidget(self.imupanel[2])
        for imupanel in self.imupanel:
            imupanel = self.imupanel[0]
            for cc in imupanel.findChildren(QComboBox):
                cc.activated.connect(self.changeMPUConfig)

        # ADC Connections
        self.ui.checkADCOn.toggled.connect(self.changeADCConfig)
        adcpanel = self.ui.adcframe.findChildren(QComboBox)
        for cc in adcpanel:
            cc.activated.connect(self.changeADCConfig)

        # Signal Generator Connections:
        self.ui.canal1.layout().addWidget(self.genpanel[0])
        self.ui.canal2.layout().addWidget(self.genpanel[1])
        self.ui.canal3.layout().addWidget(self.genpanel[2])
        self.ui.canal4.layout().addWidget(self.genpanel[3])
        for cc in self.ui.tabWidget.findChildren(QComboBox, QtCore.QRegExp("comboType.*")):
            cc.activated.connect(self.changeGeneratorConfig)
        for cc in self.ui.tabWidget.findChildren(QDoubleSpinBox, QtCore.QRegExp("spinAmpl.*|spinFreq.*")):
            cc.editingFinished.connect(self.changeGeneratorConfig)
        for cc in self.ui.tabWidget.findChildren(QCheckBox, QtCore.QRegExp("checkEnable.*")):
            cc.toggled.connect(self.plotOutConfig)
            cc.toggled.connect(self.changeGeneratorConfig)

        # PlotCfg:
        self.ui.plotCfgFrame.layout().addWidget(self.plotcfgpanel)
        self.plotcfgpanel.ui.comboPlot1.activated.connect(lambda: self.dataman.mfig.setPlotChoice(self.plotcfgpanel.ui.comboPlot1.currentIndex(),None))
        self.plotcfgpanel.ui.comboPlot2.activated.connect(lambda: self.dataman.mfig.setPlotChoice(None,self.plotcfgpanel.ui.comboPlot2.currentIndex()))
        for cc in self.plotcfgpanel.findChildren(QCheckBox):
            cc.toggled.connect(self.plotConfig)

        self.ui.checkAlgOn.setChecked(False)
        self.ui.checkAlgOn.setEnabled(False)
        self.ui.checkControle.toggled.connect(self.configControl)
        self.ui.comboCanaisControle.activated.connect(self.configControl)
        self.ui.checkAlgOn.toggled.connect(self.configAlgOn)
        self.ui.passoCtrl.setValidator(QtGui.QDoubleValidator(0.0, 1000.0, 2, self))
        self.ui.passoCtrl.editingFinished.connect(self.validateStep)
        self.ui.normCtrl.setValidator(QtGui.QDoubleValidator(0.0, 1000.0, 2, self))
        self.ui.normCtrl.editingFinished.connect(self.validateRegularization)
        self.dataman = None
        self.driver = None
        self.mfig = None
        self.ctrlfig = None
        self.ofig = None
        saveplussc = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+S"), self, self.saveDialog)
        saveplus2sc = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+Shift+S"), self, self.savePlus2)
        initstop = QtWidgets.QShortcut(QtGui.QKeySequence("Space"), self, self.kSpace)
        stepfocus = QtWidgets.QShortcut(QtGui.QKeySequence("Alt+P"), self, self.pFocus)
        self.ui.actionSavePlus.triggered.connect(self.savePlus)
        self.ui.actionDefineWorkdir.triggered.connect(self.defWorkdir)
        self.flagsaveplus = False
        self.disabledwhenrunning = []

    def pFocus(self):
        self.ui.passoCtrl.selectAll()
        self.ui.passoCtrl.setFocus()

    def kSpace(self):
        if not self.dataman.flagrodando:
            self.bInit()
        elif not self.ui.checkAlgOn.isChecked():
            self.ui.checkAlgOn.setChecked(True)
        else:
            self.bInit()

    def savePlus2(self):
        self.savePlus()
        self.bReset()

    def savePlus(self):
        try:
            if self.flagsaveplus:
                raise Exception("Dados já salvos...")
            fn = str(int(time.time() * 1000)) + '.feather'
            fname = Path(self.workdir) / fn
            ct = 0
            while fname.exists():
                fn = str(int(time.time() * 1000)) + f'{ct}.feather'
                fname = Path(self.workdir) / fn
                ct = ct + 1
                if ct > 10:
                    raise Exception("10 tentativas e arquivo ainda existe.")
            if self.dataman.globalctreadings > 0:
                if self.driver.controlMode:
                    mdatafile = Path(self.workdir) / "metacontrol.feather"
                    if mdatafile.exists():
                        mddf = pd.read_feather(mdatafile)
                    else:
                        mddf = pd.DataFrame(
                            columns=['filename', 'alg', 'mu', 'psi', 'memctrl',
                                     'tinicio', 'tipoperturb', 'amplperturb',
                                     'freqperturb', 'sensorref', 'sensorerro']
                        )
                    fdata = {
                        'filename': str(fn),
                        'alg': self.ui.comboAlgoritmo.currentText(),
                        'mu': float(self.ui.passoCtrl.text()),
                        'psi': float(self.ui.normCtrl.text()),
                        'memctrl': self.ui.spinMemCtrl.value(),
                        'tinicio': self.ui.spinTAlgOn.value(),
                        'tipoperturb': (self.ui.comboCanal1.currentText()
                                        if (self.ui.comboCanaisControle.currentIndex() == 0)
                                        else self.ui.comboCanal2.currentText()),
                        'amplperturb': (self.ui.spinAmpl1.value()    # TODO!!!!
                                        if (self.ui.comboCanaisControle.currentIndex() == 0)
                                        else self.ui.spinAmpl2.value()),
                        'freqperturb': (self.ui.spinFreq1.value()
                                        if (self.ui.comboCanaisControle.currentIndex() == 0)
                                        else self.ui.spinFreq2.value()),
                        'sensorref': self.ui.comboRef.currentText(),
                        'sensorerro': self.ui.comboErro.currentText()
                    }
                    mddf = mddf.append(fdata, ignore_index=True)
                    mddf.reset_index()
                    mddf.to_feather(mdatafile)
                    try:
                        self.dataman.salvaArquivo(fname, setsaved=True)
                    except Exception as err:
                        QMessageBox.question(self.app, "Erro!", str(err), QMessageBox.Ok)
                    self.flagsaveplus = True
                    self.ui.statusbar.showMessage("Dados salvos com sucesso...")
                else:
                    pass
            else:
                raise Exception("Sem dados para salvar.")
        except Exception as err:
            self.ui.statusbar.showMessage(str(err))

    def defWorkdir(self):
        fdg = QFileDialog(self, "Escolha Diretório de Trabalho (workdir)", getenv('HOME'))
        fdg.setFileMode(QFileDialog.DirectoryOnly)
        if fdg.exec():
            dirnames = fdg.selectedFiles()
            if dirnames is not None:
                if dirnames[0] != '':
                    self.workdir = dirnames[0]

    def readConfig(self):        
        settings = QtCore.QSettings("VibSoftware", "VibView")
        for w in self.app.allWidgets():
            # print(w.objectName())
            if ((type(w) in self.saveconfigtypes) and (settings.value(w.objectName()) is not None)):
                if (type(w) == QtWidgets.QCheckBox):
                    w.setChecked(settings.value(w.objectName()) == 'True')
                elif (type(w) == QtWidgets.QComboBox):
                    w.setCurrentIndex(int(settings.value(w.objectName())))
                elif (type(w) == QtWidgets.QDoubleSpinBox):
                    w.setValue(float(settings.value(w.objectName())))
                elif (type(w) == QtWidgets.QSpinBox):
                    w.setValue(int(settings.value(w.objectName())))
                elif (type(w) == QtWidgets.QLineEdit):
                    w.setText(settings.value(w.objectName()))
        if (settings.value("Porta") is not None):
            self.porta = settings.value("Porta")
        if (settings.value("WorkDir") is not None):
            self.workdir = settings.value("WorkDir")
        for imp in self.imupanel:
            imp.restoreState(settings)
        for gp in self.genpanel:
            gp.restoreState(settings)
        

    def writeConfig(self):
        settings = QtCore.QSettings("VibSoftware", "VibView")
        for w in self.app.allWidgets():            
            if (type(w) == QtWidgets.QCheckBox):
                settings.setValue(w.objectName(), str(w.isChecked()))
            elif (type(w) == QtWidgets.QComboBox):
                settings.setValue(w.objectName(), w.currentIndex())
            elif (type(w) == QtWidgets.QDoubleSpinBox):
                settings.setValue(w.objectName(), w.value())
            elif (type(w) == QtWidgets.QSpinBox):
                settings.setValue(w.objectName(), w.value())
            elif (type(w) == QtWidgets.QLineEdit):
                settings.setValue(w.objectName(), w.text())
        settings.setValue("Porta", self.porta)
        settings.setValue("MFig", self.mfig.getConfigString())
        settings.setValue("OFig", self.ofig.getConfigString())
        settings.setValue("CtrlFig", self.ctrlfig.getConfigString())
        settings.setValue('WorkDir', self.workdir)
        for imp in self.imupanel:
            imp.saveState(settings)
        for gp in self.genpanel:
            gp.saveState(settings)

    def setDataMan(self, dm):
        self.dataman = dm
        mfig = MyFigQtGraph(self.dataman, self)
        ctrlfig = CtrlFigQtGraph(self.dataman, self)
        self.addPlots(mfig, ctrlfig)
        outfig = FigOutputQtGraph(self.dataman, self)
        self.addPlotOut(outfig)
        self.dataman.setaFigs(mfig, ctrlfig)
        self.dataman.setaFigOut(outfig)

    def setDriver(self, drv):
        self.driver = drv
        self.changeGeneratorConfig()
        self.changeMPUConfig()
        self.changeADCConfig()
        self.configControl()

    def validateStep(self):
        try:
            passonovo = float(self.ui.passoCtrl.text())
        except Exception as exc:
            if self.driver is not None:
                self.ui.passoCtrl.setText(str(self.driver.ctrlmu))
            else:
                self.ui.passoCtrl.setText('0')

    def validateRegularization(self):
        try:
            regnovo = float(self.ui.normCtrl.text())
        except Exception as exc:
            if self.driver is not None:
                self.ui.normCtrl.setText(str(self.driver.ctrlmu))
            else:
                self.ui.normCtrl.setText('0')

    def configAlgOn(self):
        algon = self.ui.checkAlgOn.isChecked()
        algontime = float(self.ui.spinTAlgOn.value())
        if algon:
            self.driver.ctrlmu = float(self.ui.passoCtrl.text())
            self.driver.ctrlfi = float(self.ui.normCtrl.text())
        self.driver.setAlgOn(algon, algontime)
        self.ui.normCtrl.setEnabled(not algon)
        self.ui.passoCtrl.setEnabled(not algon)
        self.ui.spinTAlgOn.setEnabled(not algon)

    def configControl(self):
        self.driver.controlMode = self.ui.checkControle.isChecked()
        if self.driver.controlMode:
            state1 = (self.ui.comboCanaisControle.currentIndex() == 0)
            if state1:
                self.driver.canalControle = 1
            else:
                self.driver.canalControle = 0
            
            self.genpanel[1].setEnabled(not state1)
            
            self.genpanel[0].setEnabled(state1)
            
            if state1:
                generatorconfig1 = self.genpanel[0].getGeneratorConfig()                
                self.driver.setGeneratorConfig(0, **generatorconfig1)
                self.driver.setGeneratorConfig(1, 0, 0, self.genpanel[1].getFreqValue())
            else:
                self.driver.setGeneratorConfig(0, 0, 0, self.genpanel[0].getFreqValue())
                generatorconfig2 = self.genpanel[1].getGeneratorConfig()
                self.driver.setGeneratorConfig(1, **generatorconfig2)
            self.driver.setControlConfig(
                self.ui.comboAlgoritmo.currentIndex(),
                int(self.ui.spinMemCtrl.value()),
                float(self.ui.passoCtrl.text()),
                float(self.ui.normCtrl.text()),
                self.ui.comboRef.currentIndex(),
                self.ui.comboErro.currentIndex()
            )
            if (self.mfig is not None):
                self.ctrlfig.show()
                self.mfig.hide()

        else:
            self.genpanel[1].setEnabled(True)
            self.genpanel[0].setEnabled(True)
            self.changeGeneratorConfig()
            if (self.ctrlfig is not None):
                self.mfig.show()
                self.ctrlfig.hide()

    def plotOutConfig(self):
        self.ofig.dacenable = [aa.isGeneratorOn() for aa in self.genpanel]

    def plotConfig(self):
        self.mfig.accEnable = self.plotcfgpanel.getAccEnableList()
        self.mfig.gyroEnable = self.plotcfgpanel.getGyroEnableList()
        self.ctrlfig.plotSetup([self.ui.comboRef.currentIndex(), self.ui.comboErro.currentIndex()])

    def changeGeneratorConfig(self):
        for k in range(4):
            generatorconfig = self.genpanel[k].getGeneratorConfig()
            self.driver.setGeneratorConfig(k, **generatorconfig)

    def changeMPUConfig(self):
        if self.driver is not None:
            for id in range(3):
                self.driver.setIMUConfig(id,self.imupanel[id].getIMUConfig())

    def changeADCConfig(self):
        if self.driver is not None:
            adcconfig = [1 if self.ui.checkADCOn.isChecked() else 0,
                         self.ui.comboADCChannel.currentIndex(),
                         self.ui.comboRangeADC.currentIndex(),
                         self.ui.comboADCRate.currentIndex()]
            self.driver.setADCConfig(adcconfig)

    def addPlots(self, mfig, ctrlfig):
        settings = QtCore.QSettings("VibSoftware", "VibView")
        self.mfig = mfig
        self.ctrlfig = ctrlfig
        self.ui.plotOutLayout.addWidget(self.mfig)
        self.ui.plotOutLayout.addWidget(self.ctrlfig)
        if self.ui.checkControle.isChecked():
            self.mfig.hide()
        else:
            self.ctrlfig.hide()
        aux = settings.value('MFig')
        if aux is not None:
            self.mfig.parseConfigString(aux)
        aux = settings.value('CtrlFig')
        if aux is not None:
            self.ctrlfig.parseConfigString(aux)
        self.plotConfig()

    def addPlotOut(self, ofig):
        self.ofig = ofig
        settings = QtCore.QSettings("VibSoftware", "VibView")
        aux = settings.value('OFig')
        if aux is not None:
            self.ofig.parseConfigString(aux)
        self.ui.plotLayout2.addWidget(self.ofig)
        # self.ofig.draw()
    
    def bInit(self):
        if self.dataman.flagrodando:
            self.dataman.ParaLeituras()
        else:
            self.flagsaveplus = False
            self.configControl()
            self.changeGeneratorConfig()                   
            self.changeMPUConfig()
            self.changeADCConfig()
            self.plotConfig()
            self.plotOutConfig()

            self.disabledwhenrunning = self.imupanel + [self.ui.checkControle,self.ui.comboCanaisControle,
                                   self.ui.comboRef,self.ui.comboErro,self.ui.comboAlgoritmo,self.ui.spinMemCtrl,
                                   self.ui.checkADCOn,self.ui.comboADCChannel,self.ui.comboRangeADC,self.ui.comboADCRate]
            for cc in self.disabledwhenrunning: 
                cc.setEnabled(False)

            if self.ui.checkControle.isChecked():
                self.ui.checkAlgOn.setEnabled(True)

            if self.driver.adcconfig[0] == 0:
                self.mfig.removeADCPlot()
            else:
                self.mfig.addADCPlot()

            self.dataman.IniciaLeituras()

    # def bPara(self):
    #     self.dataman.ParaLeituras()

    def readingsStopped(self):
        for cc in self.disabledwhenrunning:
            cc.setEnabled(True)
        self.ui.checkAlgOn.setEnabled(False)
        self.ui.checkAlgOn.setChecked(False)

    def bReset(self):
        if self.dataman.flagrodando:
            self.ui.statusbar.showMessage("Leituras sendo realizadas, dados não podem ser apagados.")
            return
        if not self.dataman.flagsaved:
            buttonReply = QMessageBox.question(self, 'Atenção!', "Dados não salvos poderão ser apagados, confirma?",
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                self.dataman.ResetaDados()
                self.ui.statusbar.clearMessage()
            else:
                self.ui.statusbar.showMessage("Cancelado...")
        else:
            self.dataman.ResetaDados()
            self.ui.statusbar.clearMessage()

    def setaPorta(self, portasel):
        self.porta = portasel
        print(self.porta)
        for acc in self.ui.menuSelecionar_Porta.actions():
            actualFont = acc.font()
            actualFont.setBold(acc.text() == self.porta)
            acc.setFont(actualFont)
        self.ui.statusbar.clearMessage()

    def openWorkdirManager(self):
        if not self.dataman.flagrodando:
            self.wdman = WorkdirManager(self.workdir)
            self.wdman.showWorkdirManager()

    def openUploadDialog(self):
        if not self.dataman.flagrodando:
            self.upd = MyUploadDialog(self.driver)
            self.upd.showUploadDialog()

    def saveDialog(self):
        if self.dataman.flagrodando:
            self.ui.statusbar.showMessage("Leituras sendo realizadas, dados não podem ser salvos.")
            return
        filename = QFileDialog.getSaveFileName(self, "Salvar Arquivo", getenv('HOME'), 'feather (*.feather)')
        if (filename[0] != ''):
            try:
                self.dataman.salvaArquivo(filename[0], True)
            except Exception as err:
                QMessageBox.question(self.app, "Erro!", str(err), QMessageBox.Ok)

    def closeEvent(self, event):
        if not event:
            self.writeConfig()
            event = QtGui.QCloseEvent()
            event.accept = self.close
            event.ignore = (lambda *args: None)
        if self.dataman.flagrodando:
            self.ui.statusbar.showMessage("Pare as leituras antes de fechar...")
            event.ignore()
        elif not self.dataman.flagsaved:
            reply = QMessageBox.question(self, 'Saindo', 'Existem dados não salvos, deseja mesmo sair?',
                                         QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.writeConfig()
                event.accept()
            else:
                event.ignore()
        else:
            self.writeConfig()
            event.accept()
