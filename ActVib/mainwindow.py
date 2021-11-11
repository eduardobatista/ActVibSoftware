from pathlib import Path
from os import getenv
import time

import pandas as pd

from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtWidgets import QMessageBox, QFileDialog, QCheckBox, QComboBox, QDoubleSpinBox, QSpinBox

from .VibViewWindow import Ui_MainWindow

from .others import (MyFigQtGraph, CtrlFigQtGraph, FigOutputQtGraph, WorkdirManager, MyUploadDialog)

from .panels import (IMUPanel,GeneratorPanel,PlotCfgPanel,ControlPanel,ADCPanel)

class mainwindow(QtWidgets.QMainWindow):

    def __init__(self, app, driver, dataman):
        super(mainwindow, self).__init__()
        self.app = app
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.cw = self.ui.centralwidget
        self.porta = "COM3"
        self.TSampling = 4   # 4 ms is the default
        self.workdir = "D://"
        self.dataman = dataman
        self.driver = driver
        self.saveconfigtypes = [QtWidgets.QCheckBox, QtWidgets.QComboBox,
                                QtWidgets.QDoubleSpinBox, QtWidgets.QSpinBox, QtWidgets.QLineEdit]
        self.imupanel = [IMUPanel(idd) for idd in range(3)]
        self.genpanel = [GeneratorPanel(idd) for idd in range(4)]
        self.adcpanel = ADCPanel()

        self.plotcfgpanel = PlotCfgPanel()
        self.ctrlpanel = ControlPanel()
        self.readConfig()        
        self.ui.bInit.clicked.connect(self.bInit)
        self.ui.bLimpar.clicked.connect(self.bReset)

        self.mapper = QtCore.QSignalMapper(self)
        for acc in self.ui.menuSelecionar_Porta.actions():
            self.mapper.setMapping(acc, acc.text())
            acc.triggered.connect(self.mapper.map)
        self.mapper.mapped['QString'].connect(self.setaPorta)

        self.mapper2 = QtCore.QSignalMapper(self)
        for sra in self.ui.menuSampling_Rate.actions():
            self.mapper2.setMapping(sra, sra.text())
            sra.triggered.connect(self.mapper2.map)
        self.mapper2.mapped['QString'].connect(self.setSampling)

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
        self.ui.adctab.layout().addWidget(self.adcpanel)
        # self.ui.checkADCOn.toggled.connect(self.changeADCConfig)
        # adcpanel = self.ui.adcframe.findChildren(QComboBox)
        # for cc in adcpanel:
        #     cc.activated.connect(self.changeADCConfig)

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
        self.plotcfgpanel.ui.comboPlot1.activated.connect(lambda: self.mfig.setPlotChoice(self.plotcfgpanel.ui.comboPlot1.currentIndex(),None))
        self.plotcfgpanel.ui.comboPlot2.activated.connect(lambda: self.mfig.setPlotChoice(None,self.plotcfgpanel.ui.comboPlot2.currentIndex()))
        for cc in self.plotcfgpanel.findChildren(QCheckBox):
            cc.toggled.connect(self.plotConfig)
        
        # ControlPanel:
        self.ui.controlFrame.layout().addWidget(self.ctrlpanel)  
        self.ctrlpanel.connectControlChanged(self.configControl)      
        # self.ui.comboCanaisControle.activated.connect(self.configControl)
        self.ctrlpanel.ui.checkAlgOn.toggled.connect(self.configAlgOn)
        # self.ui.passoCtrl.setValidator(QtGui.QDoubleValidator(0.0, 1000.0, 2, self))
        # self.ui.passoCtrl.editingFinished.connect(self.validateStep)
        # self.ui.normCtrl.setValidator(QtGui.QDoubleValidator(0.0, 1000.0, 2, self))
        # self.ui.normCtrl.editingFinished.connect(self.validateRegularization)

        
        self.dataman.updateFigures.connect(self.updateFigs)
        self.dataman.reset.connect(self.dataReset)
        self.dataman.statusMessage.connect(self.statusMessage)
        self.dataman.stopped.connect(self.readingsStopped)

        self.mfig = MyFigQtGraph(self.dataman, self)
        self.ctrlfig = CtrlFigQtGraph(self.dataman, self)        
        self.ofig = FigOutputQtGraph(self.dataman, self)
        self.addPlots()

        self.changeGeneratorConfig()
        self.changeMPUConfig()
        self.changeADCConfig()
        self.configControl()

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
            self.setaPorta(self.porta)
        if (settings.value("TSampling") is not None):
            self.setSampling(settings.value("TSampling"))            
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
        settings.setValue("TSampling", str(self.TSampling) + " ms")
        settings.setValue("MFig", self.mfig.getConfigString())
        settings.setValue("OFig", self.ofig.getConfigString())
        settings.setValue("CtrlFig", self.ctrlfig.getConfigString())
        settings.setValue('WorkDir', self.workdir)
        for imp in self.imupanel:
            imp.saveState(settings)
        for gp in self.genpanel:
            gp.saveState(settings)


    def statusMessage(self, msg):
        if msg is None:
            self.ui.statusbar.clearMessage()
        else:
            self.ui.statusbar.showMessage(msg) 


    def updateFigs(self):
        self.ui.elapsedTime.setText(f'{int(self.dataman.readtime)} s / {self.dataman.maxtime} s')
        self.ui.controlTime.setText(f'{self.dataman.realtime:.3f} s')
        self.ui.sampleTime.setText(f'{self.driver.calctime[0]:.0f}/{self.driver.calctime[1]:.0f}/{self.driver.calctime[2]:.0f} us')
        if self.driver.controlMode:
            self.ctrlfig.updateFig()
        else:
            self.mfig.updateFig()
        self.ofig.updateFig()

    
    def dataReset(self):
        self.ui.elapsedTime.setText('0 s')
        self.ui.controlTime.setText('0 s')
        self.ui.sampleTime.setText('0 us')
        self.mfig.updateFig(self.driver.controlMode, [self.driver.refid, self.driver.erroid])
        self.ofig.updateFig()
        self.ctrlfig.updateFig()


    def configAlgOn(self):
        algon = self.ctrlpanel.ui.checkAlgOn.isChecked()
        algontime = float(self.ctrlpanel.ui.spinTAlgOn.value())
        if algon:
            self.driver.ctrlmu = float(self.ctrlpanel.ui.passoCtrl.text())
            self.driver.ctrlfi = float(self.ctrlpanel.ui.normCtrl.text())
        self.driver.setAlgOn(algon, algontime)
        self.ctrlpanel.ui.normCtrl.setEnabled(not algon)
        self.ctrlpanel.ui.passoCtrl.setEnabled(not algon)
        self.ctrlpanel.ui.spinTAlgOn.setEnabled(not algon)


    def configControl(self):        
        self.driver.controlMode = self.ctrlpanel.isControlOn()
        if self.driver.controlMode:
            self.driver.controlChannel = self.ctrlpanel.getControlChannel()
            self.driver.perturbChannel = self.ctrlpanel.getPerturbChannel()
            for gg in self.genpanel:
                gg.setEnabled(True)
            self.genpanel[self.driver.controlChannel].setEnabled(False)
            self.driver.setControlConfig( **self.ctrlpanel.getControlConfiguration() )
            if (self.mfig is not None):
                self.ctrlfig.show()
                self.mfig.hide()
        else:
            for gg in self.genpanel:
                gg.setEnabled(True)
            self.changeGeneratorConfig()
            if (self.ctrlfig is not None):
                self.mfig.show()
                self.ctrlfig.hide()


    def plotOutConfig(self):
        self.ofig.dacenable = [aa.isGeneratorOn() for aa in self.genpanel]


    def plotConfig(self):
        self.mfig.accEnable = self.plotcfgpanel.getAccEnableList()
        self.mfig.gyroEnable = self.plotcfgpanel.getGyroEnableList()
        self.ctrlfig.plotSetup([self.ctrlpanel.ui.comboRef.currentIndex(), self.ctrlpanel.ui.comboErro.currentIndex()])


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
            self.driver.setADCConfig(self.adcpanel.getADCConfig())
        if self.mfig is not None:
            self.mfig.adcEnableMap = self.driver.adcenablemap

    def addPlots(self):
        settings = QtCore.QSettings("VibSoftware", "VibView")
        self.ui.plotOutLayout.addWidget(self.mfig)
        self.ui.plotOutLayout.addWidget(self.ctrlfig)
        if self.ctrlpanel.isControlOn():
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

        settings = QtCore.QSettings("VibSoftware", "VibView")
        aux = settings.value('OFig')
        if aux is not None:
            self.ofig.parseConfigString(aux)
        self.ui.plotLayout2.addWidget(self.ofig)
        
    
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

            self.disabledwhenrunning = self.imupanel + [self.ctrlpanel,self.adcpanel]
            for cc in self.disabledwhenrunning: 
                cc.setEnabled(False)

            if self.ctrlpanel.isControlOn():
                self.ctrlpanel.ui.checkAlgOn.setEnabled(True)

            if (self.driver.adcconfig[0] & 0x0F) == 0:
                self.mfig.removeADCPlot()
            else:
                self.mfig.addADCPlot()

            self.mfig.setPlotChoice(self.plotcfgpanel.ui.comboPlot1.currentIndex(),self.plotcfgpanel.ui.comboPlot2.currentIndex())

            for k in range(3):
                self.driver.setIMUConfig(k,self.imupanel[k].getIMUConfig())
            self.changeADCConfig()

            self.driver.setPort(self.porta)
            self.dataman.IniciaLeituras()


    def readingsStopped(self):
        for cc in self.disabledwhenrunning:
            cc.setEnabled(True)
        self.ctrlpanel.ui.checkAlgOn.setEnabled(False)
        self.ctrlpanel.ui.checkAlgOn.setChecked(False)

    def bReset(self):
        if self.dataman.flagrodando:
            self.ui.statusbar.showMessage("Leituras sendo realizadas, dados não podem ser apagados.")
            return
        if not self.dataman.flagsaved:
            buttonReply = QMessageBox.question(self, 'Atenção!', "Dados não salvos poderão ser apagados, confirma?",
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                self.dataman.ResetaDados(self.TSampling/1000)
                self.ui.statusbar.clearMessage()
            else:
                self.ui.statusbar.showMessage("Cancelado...")
        else:
            self.dataman.ResetaDados(self.TSampling/1000)
            self.ui.statusbar.clearMessage()

    def setSampling(self, selsampling):
        if self.dataman.flagrodando or (not self.dataman.flagsaved):
            self.ui.statusbar.setMessage("Not allowed when running or with unsaved data.")
        else:
            if selsampling.startswith(">"):
                selsampling = selsampling[1:]
            self.TSampling = int(selsampling[0])
            for sra in self.ui.menuSampling_Rate.actions():
                if sra.text().endswith(selsampling):
                    sra.setText(f">{selsampling}")
                else:
                    if sra.text().startswith(">"):
                        sra.setText(sra.text()[1:])
            self.dataman.ResetaDados(self.TSampling/1000)
            self.ui.statusbar.clearMessage()
            
        
    def setaPorta(self, portasel):
        if not self.dataman.flagrodando:
            if portasel.startswith(">"):
                portasel = portasel[1:]
            self.porta = portasel
            for acc in self.ui.menuSelecionar_Porta.actions():
                if acc.text().endswith(portasel):
                    acc.setText(f">{portasel}")
                else:
                    if acc.text().startswith(">"):
                        acc.setText(acc.text()[1:])
            self.ui.statusbar.clearMessage()
        else: 
            self.ui.statusbar.setMessage("Not allowed when running.")

    def openWorkdirManager(self):
        if not self.dataman.flagrodando:
            self.wdman = WorkdirManager(self.workdir)
            self.wdman.showWorkdirManager()

    def openUploadDialog(self):
        if not self.dataman.flagrodando:
            self.driver.setPort(self.porta)
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
