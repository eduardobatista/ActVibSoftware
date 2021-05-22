from PyQt5 import (QtCore, QtWidgets)
from IMUPanel import Ui_IMUPanel
from GeneratorPanel import Ui_GeneratorPanel
from PlotCfgPanel import Ui_PlotCfgForm


class StateSaver:

    def saveState(self, settings: QtCore.QSettings):
        if self.saveprefix is None:
            self.saveprefix = ""
        wdgs = self.findChildren(QtWidgets.QComboBox) 
        for ww in wdgs:
            keyval = f'{self.saveprefix}{ww.objectName()}'
            settings.setValue(keyval, ww.currentIndex())
            settings.setValue(f'EN{keyval}', str(ww.isEnabled()))
        wdgs = self.findChildren(QtWidgets.QCheckBox)
        for ww in wdgs:
            keyval = f'{self.saveprefix}{ww.objectName()}'
            settings.setValue(keyval, str(ww.isChecked()))
            settings.setValue(f'EN{keyval}', str(ww.isEnabled()))
        wdgs = self.findChildren(QtWidgets.QDoubleSpinBox) + self.findChildren(QtWidgets.QSpinBox)
        for ww in wdgs:
            keyval = f'{self.saveprefix}{ww.objectName()}'
            # print(f'{keyval} - {ww.isEnabled()}')
            settings.setValue(keyval, ww.value())
            settings.setValue(f'EN{keyval}', str(ww.isEnabled()))

    
    def restoreState(self, settings: QtCore.QSettings):
        if self.saveprefix is None:
            self.saveprefix = ""

        wdgs = self.findChildren(QtWidgets.QComboBox,QtCore.QRegExp("combo.*")) 
        for ww in wdgs:
            keyval = f'{self.saveprefix}{ww.objectName()}'
            if settings.value(keyval) is not None:
                ww.setCurrentIndex(int(settings.value(keyval)))
            if settings.value(f'EN{keyval}') is not None:
                ww.setEnabled(settings.value(f'EN{keyval}') == 'True')

        wdgs = self.findChildren(QtWidgets.QCheckBox,QtCore.QRegExp("check.*"))
        for ww in wdgs:
            keyval = f'{self.saveprefix}{ww.objectName()}'
            if settings.value(keyval) is not None:
                ww.setChecked(settings.value(keyval) == 'True')
            if settings.value(f'EN{keyval}') is not None:
                ww.setEnabled(settings.value(f'EN{keyval}') == 'True')
        
        wdgs = self.findChildren(QtWidgets.QDoubleSpinBox)
        for ww in wdgs:
            keyval = f'{self.saveprefix}{ww.objectName()}'
            # aux = settings.value(f'EN{keyval}')
            # print(f'{keyval} - {aux}')
            if settings.value(keyval) is not None:
                ww.setValue(float(settings.value(keyval)))
            if settings.value(f'EN{keyval}') is not None:
                ww.setEnabled(settings.value(f'EN{keyval}') == 'True')
        
        wdgs = self.findChildren(QtWidgets.QSpinBox)
        for ww in wdgs:
            keyval = f'{self.saveprefix}{ww.objectName()}'
            if settings.value(keyval) is not None:
                ww.setValue(int(settings.value(keyval)))
            if settings.value(f'EN{keyval}') is not None:
                ww.setEnabled(settings.value(f'EN{keyval}') == 'True')




class GeneratorPanel(QtWidgets.QWidget,StateSaver):

    def __init__(self, id: int):
        super().__init__()
        self.id = id
        self.ui = Ui_GeneratorPanel()
        self.ui.setupUi(self)
        self.saveprefix = f'GEN{id}'
        self.ui.comboType.activated.connect(self.typechanged)
    
    def isGeneratorOn(self):
        return self.ui.checkEnable.isEnabled()

    def typechanged(self):
        idx = self.ui.comboType.currentIndex()
        if idx == 0:  # Noise
            for aa in [self.ui.spinFreq,self.ui.chirpDeltaI,self.ui.chirpTfim,self.ui.chirpDeltaF,self.ui.chirpA2,self.ui.chirpTinicio]:
                aa.setEnabled(False)
            self.ui.spinAmpl.setEnabled(True)
        elif idx == 1:  # Harmonic
            for aa in [self.ui.chirpDeltaI,self.ui.chirpTfim,self.ui.chirpDeltaF,self.ui.chirpA2,self.ui.chirpTinicio]:
                aa.setEnabled(False)
            self.ui.spinAmpl.setEnabled(True)
            self.ui.spinFreq.setEnabled(True)
        elif idx == 2:  # Chirp
            for aa in [self.ui.spinAmpl,self.ui.spinFreq,self.ui.chirpDeltaI,self.ui.chirpTfim,self.ui.chirpDeltaF,self.ui.chirpA2,self.ui.chirpTinicio]:
                aa.setEnabled(True)
        elif idx == 3:  # Step
            for aa in [self.ui.chirpDeltaI,self.ui.chirpDeltaF,self.ui.chirpA2,self.ui.spinFreq]:
                aa.setEnabled(False)
            for aa in [self.ui.chirpTinicio,self.ui.chirpTfim,self.ui.spinAmpl]:
                aa.setEnabled(True)
    
    def setEnabled(self,en):
        self.ui.checkEnable.setEnabled(en)
        self.ui.comboType.setEnabled(en)
        self.ui.spinAmpl.setEnabled(en)
        self.ui.spinFreq.setEnabled(en)
    
    def getGeneratorConfig(self):
        if self.ui.checkEnable.isChecked():
            generatorconfig = {'tipo': self.ui.comboType.currentIndex(),
                                'amp': self.ui.spinAmpl.value(),
                                'freq': self.ui.spinFreq.value()}
            if self.ui.comboType.currentIndex() == 2:  # Chirp
                generatorconfig['chirpconf'] = [self.ui.chirpTinicio.value(),
                                                self.ui.chirpDeltaI.value(),
                                                self.ui.chirpTfim.value(),
                                                self.ui.chirpDeltaF.value(),
                                                self.ui.chirpA2.value()]
            return generatorconfig
        else:
            return {'tipo': 0, 'amp': 0, 'freq': 0}
    
    def getFreqValue(self):
        return self.ui.spinFreq.value()


class PlotCfgPanel(QtWidgets.QWidget,StateSaver):
    def __init__(self):
        super().__init__()
        self.ui = Ui_PlotCfgForm()
        self.ui.setupUi(self)
        self.checks = [self.ui.checkAccX,self.ui.checkAccY,self.ui.checkAccZ,
                       self.ui.checkGyroX,self.ui.checkGyroY,self.ui.checkGyroZ]
        self.saveprefix = 'PlotCfg'

    def getAccEnableList(self):
        return [self.ui.checkAccX.isChecked(),
                self.ui.checkAccY.isChecked(),
                self.ui.checkAccZ.isChecked()]

    def getGyroEnableList(self):
        return [self.ui.checkGyroX.isChecked(),
                self.ui.checkGyroY.isChecked(),
                self.ui.checkGyroZ.isChecked()]

class IMUPanel(QtWidgets.QWidget,StateSaver):

    def __init__(self, id: int):
        super().__init__()
        self.ui = Ui_IMUPanel()
        self.ui.setupUi(self)
        self.ui.comboType.activated.connect(self.typechanged)
        self.ui.comboAddress.highlighted.connect(self.addresshighlight)
        self.saveprefix = f'IMU{id}'

    '''
        IMU config data:

        Byte 0 -| Enabled (1 bit) (LSB)
                | Type: MPU, LSM (1 bit)
                | Bus selection (2 bits, for future expansion)

        Byte 1 - Address (8 bits)
                
        Byte 2 -| AccRange (2 bits) (LSBs)
                | GyroRange (3 bits) (LSM Gyro have 5 options)
                | Filter config (3 bits)
    '''
    def getIMUConfig(self):
        configbytes = []        
        # Byte 0:
        configbytes.append( (self.ui.comboBus.currentIndex()<<2) + (int(self.ui.comboType.currentIndex() == 2) << 1) +  int(self.ui.comboType.currentIndex() > 0)  )
        # Byte 1:
        configbytes.append( int(str(self.ui.comboAddress.currentText())[2:],16) )
        # Byte 2:
        configbytes.append( (self.getMPUFilter()<<5) + (self.getGyroRange()<<2) + self.getAccRange() )
        return configbytes

    def getMPUAddress(self):
        return self.ui.comboAddress.currentIndex()
    
    def getMPUFilter(self):
        return self.ui.comboFilter.currentIndex()
    
    def getLSMFilter(self):
        return self.ui.comboFilter2.currentIndex()

    def getAccRange(self):
        return self.ui.comboAccRange.currentIndex()

    def getGyroRange(self):
        aux = self.ui.comboGyroRange.currentIndex()
        if self.ui.comboType.currentIndex() == 1:            
            if aux < 1: 
                self.ui.comboGyroRange.setCurrentIndex(1)
                aux = 1
            return aux
        elif self.ui.comboType.currentIndex() == 2:
            return aux
        else:
            return 0
    
    def setEnabled(self,en):
        if self.ui.comboType.currentIndex() > 0:
            cmps = [self.ui.comboAddress,self.ui.comboAccRange,self.ui.comboGyroRange,
                    self.ui.comboFilter,self.ui.comboBus,self.ui.comboType,self.ui.comboFilter2]
            for cc in cmps:
                cc.setEnabled(en)
        else:
            self.ui.comboType.setEnabled(en)
    
    def isIMUEnabled(self):
        return self.ui.comboType.currentIndex() > 0

    def addresshighlight(self):
        if self.ui.comboType.currentIndex() == 1:
            self.ui.comboAddress.model().item(0).setEnabled(True)
            self.ui.comboAddress.model().item(1).setEnabled(True)
            self.ui.comboAddress.model().item(2).setEnabled(False)
            self.ui.comboAddress.model().item(3).setEnabled(False)
            self.ui.comboGyroRange.model().item(0).setEnabled(False)
            if self.ui.comboGyroRange.currentIndex() == 0:
                self.ui.comboGyroRange.setCurrentIndex(1)
            if self.ui.comboAddress.currentIndex() > 1:
                self.ui.comboAddress.setCurrentIndex(0)
            self.ui.comboFilter.setEnabled(True)
            self.ui.comboFilter2.setEnabled(False)
        elif self.ui.comboType.currentIndex() == 2:
            self.ui.comboAddress.model().item(0).setEnabled(False)
            self.ui.comboAddress.model().item(1).setEnabled(False)
            self.ui.comboAddress.model().item(2).setEnabled(True)
            self.ui.comboAddress.model().item(3).setEnabled(True)
            self.ui.comboGyroRange.model().item(0).setEnabled(True)
            if self.ui.comboAddress.currentIndex() < 2:
                self.ui.comboAddress.setCurrentIndex(2)
            self.ui.comboFilter.setEnabled(False)
            self.ui.comboFilter2.setEnabled(True)

    def typechanged(self):
        cmps = [self.ui.comboAddress,self.ui.comboAccRange,self.ui.comboGyroRange,self.ui.comboFilter,self.ui.comboBus]
        if self.ui.comboType.currentIndex() == 0:
            enabled = False
        else:
            enabled = True
        for cc in cmps:
            cc.setEnabled(enabled)
        self.addresshighlight()
        
        


