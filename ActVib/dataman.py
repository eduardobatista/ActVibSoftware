"""
    Data Manager Module
"""
from threading import Thread
import time
import numpy as np
import pandas as pd


class dataman:

    def __init__(self, driver, mwindow):
        self.plotupdatesec = 1
        self.samplingperiod = 4e-3  # 2.5e-3 #4e-3
        self.wsize = 200000
        self.driver = driver
        self.timereads = np.zeros(self.wsize)
        self.flagparar = True
        self.flagrodando = False
        self.mfig = None
        self.ctrlfig = None
        self.ofig = None
        self.flagsaved = True
        self.ctreadings = 0
        self.globalctreadings = 0
        self.readtime = 0
        self.accdata = [[np.zeros(self.wsize), np.zeros(self.wsize), np.zeros(self.wsize)],
                        [np.zeros(self.wsize), np.zeros(self.wsize), np.zeros(self.wsize)],
                        [np.zeros(self.wsize), np.zeros(self.wsize), np.zeros(self.wsize)]]
        self.gyrodata = [[np.zeros(self.wsize), np.zeros(self.wsize), np.zeros(self.wsize)],
                        [np.zeros(self.wsize), np.zeros(self.wsize), np.zeros(self.wsize)],
                        [np.zeros(self.wsize), np.zeros(self.wsize), np.zeros(self.wsize)]]
        self.dacoutdata = [np.zeros(self.wsize), np.zeros(self.wsize), np.zeros(self.wsize), np.zeros(self.wsize)]
        self.adcdata = np.zeros(self.wsize)
        self.xrefdata = np.zeros(self.wsize)
        self.xerrodata = np.zeros(self.wsize)
        self.maxtime = int(self.wsize * self.samplingperiod)
        self.realtime = 0.0
        self.mwindow = mwindow

    def setaFigs(self, fig, cfig):
        self.mfig = fig
        self.ctrlfig = cfig

    def setaFigOut(self, fig):
        self.ofig = fig

    def ParaLeituras(self):
        self.flagparar = True
        self.mwindow.ui.statusbar.clearMessage()

    def IniciaLeituras(self):
        self.mwindow.ui.statusbar.clearMessage()        
        self.flagparar = False
        self.mythread = Thread(target=self.LeDados)
        self.mythread.start()

    def LeDados(self):
        try:
            trd = Thread(target=self.updateFigs)
            trd.start()
            ctrlmode = self.driver.controlMode
            self.flagrodando = True
            self.driver.openSerial()
            self.driver.handshake()
            if ctrlmode:
                self.driver.writeSensorChoice(0)
                self.driver.initHardware()
                self.driver.writeMPUScales()
                self.driver.writeMPUFilter()
                self.driver.writeSensorChoice(1)
                self.driver.initHardware()
                self.driver.writeMPUScales()
                self.driver.writeMPUFilter()
                self.driver.writeControlConfig()
                self.driver.setAlgOn(False, 0, forcewrite=True)
                self.driver.writeAlgOn()
                self.driver.writeGeneratorConfig(id=0)
                self.driver.writeGeneratorConfig(id=1)
                self.driver.startControl()
            else:
                # self.driver.writeSensorChoice()
                # self.driver.initHardware()
                # self.driver.writeMPUScales()
                # self.driver.writeMPUFilter()
                self.driver.enabledIMUs = 0
                for k in range(3):
                    self.driver.writeIMUConfig(k)
                    if self.mwindow.imupanel[k].isIMUEnabled():
                        self.driver.initHardware(k)
                        self.driver.enabledIMUs += 1
                self.driver.writeADCConfig()
                for k in range(4):
                    self.driver.writeGeneratorConfig(id=k)
                self.driver.startReadings()
            self.flagsaved = False
            self.ctreadings = 0
            self.starttime = round(time.time() * 1000) / 1000
            lastfigrefresh = 0
            if self.globalctreadings == 0:
                self.globalstarttime = self.starttime
            timedelta = self.starttime - self.globalstarttime
            while not self.flagparar:
                self.driver.getReading()
                self.readtime = self.ctreadings * self.samplingperiod + timedelta
                self.timereads[self.globalctreadings] = self.readtime
                if ctrlmode:
                    self.xrefdata[self.globalctreadings] = self.driver.xref
                    self.xerrodata[self.globalctreadings] = self.driver.xerro
                else:
                    for j in range(self.driver.enabledIMUs):
                        for k in range(3):
                            self.accdata[j][k][self.globalctreadings] = self.driver.accreadings[j][k]
                            self.gyrodata[j][k][self.globalctreadings] = self.driver.gyroreadings[j][k]
                self.dacoutdata[0][self.globalctreadings] = self.driver.dacout[0]
                self.dacoutdata[1][self.globalctreadings] = self.driver.dacout[1]
                self.dacoutdata[2][self.globalctreadings] = self.driver.dacout[2]
                self.dacoutdata[3][self.globalctreadings] = self.driver.dacout[3]
                self.adcdata[self.globalctreadings] = self.driver.adcin
                self.ctreadings += 1
                self.globalctreadings += 1
                if (self.readtime - lastfigrefresh) >= self.plotupdatesec:
                    # print(self.readtime)
                    self.realtime = self.readtime - (time.time() - self.starttime)
                    lastfigrefresh = self.readtime
                    if self.driver.algonchanged and (self.readtime >= self.driver.algontime):
                        self.driver.writeAlgOn()
                        # print("AlgOn!!!")
                    for k in range(4):
                        if not self.driver.genConfigWritten[k]:
                            self.driver.writeGeneratorConfig(k)
                    if not trd.isAlive():
                        trd = Thread(target=self.updateFigs)
                        trd.start()
                    # print(f'{int(self.driver.calctime)} us')
                ctaux = 0
            self.driver.stopReadings()
            self.mwindow.readingsStopped()
            self.flagrodando = False
            self.flagparar = False
            # app.save(srcdir,"backup" + str(time.time()) + ".txt")
        except Exception as err:
            if self.driver.serial.isOpen():
                self.driver.stopReadings()
            self.flagrodando = False
            self.mwindow.ui.statusbar.showMessage("Erro: " + str(err))
            self.mwindow.readingsStopped()

    def updateFigs(self):
        self.mwindow.ui.elapsedTime.setText(f'{int(self.readtime)} s / {self.maxtime} s')
        self.mwindow.ui.controlTime.setText(f'{self.realtime:.3f} s')
        if self.driver.controlMode:
            self.ctrlfig.updateFig([self.driver.refid, self.driver.erroid])
        else:
            self.mfig.updateFig()
        self.ofig.updateFig()
        # application.ui.progressBar.setValue(self.globalctreadings // 2000)

    def ResetaDados(self):
        self.maxv = 1000
        self.flagsaved = True
        self.globalctreadings = 0
        self.mfig.updateFig(self.driver.controlMode, [self.driver.refid, self.driver.erroid])
        self.ofig.updateFig()
        self.ctrlfig.updateFig()
        self.mwindow.ui.elapsedTime.setText('0 s')
        self.mwindow.ui.controlTime.setText('0 s')

    def salvaArquivo(self, filename, setsaved):
        if self.driver.controlMode:
            limf = self.globalctreadings
            df = pd.DataFrame({
                'Tempo (s)': self.timereads[0:limf],
                'Perturbacao': self.dacoutdata[0][0:limf],
                'Controle': self.dacoutdata[1][0:limf],
                'Referencia': self.xrefdata[0:limf],
                'Erro': self.xerrodata[0:limf]
            })
            # df.to_csv(filename,index=False)
            df.to_feather(filename)
        else:
            limf = self.globalctreadings
            df = pd.DataFrame({
                "Tempo (s)": self.timereads[0:limf],
                "Acc X": self.accdata[0][0][0:limf],
                "Acc Y": self.accdata[0][1][0:limf],
                "Acc Z": self.accdata[0][2][0:limf],
                "Gyro X": self.gyrodata[0][0][0:limf],
                "Gyro Y": self.gyrodata[0][1][0:limf],
                "Gyro Z": self.gyrodata[0][2][0:limf],
                "DAC 1": self.dacoutdata[0][0:limf],
                "DAC 2": self.dacoutdata[1][0:limf],
                "DAC 3": self.dacoutdata[2][0:limf],
                "DAC 4": self.dacoutdata[3][0:limf],
                "ADC in": self.adcdata[0:limf]
            })
            df.to_feather(filename)
        self.flagsaved = setsaved
