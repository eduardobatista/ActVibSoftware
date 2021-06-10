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
        # self.samplingperiod = 2e-3
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
        self.adcdata = [np.zeros(self.wsize), np.zeros(self.wsize), np.zeros(self.wsize), np.zeros(self.wsize)]
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
            for k in range(3):
                self.driver.setIMUConfig(k,self.mwindow.imupanel[k].getIMUConfig())
                self.driver.writeIMUConfig(k)
                if self.driver.IMUEnableFlags[k]:
                    self.driver.initHardware(k)
            # TODO: merge the following 2 calls?
            self.mwindow.changeADCConfig()
            self.driver.writeADCConfig()
            for k in range(4):
                self.driver.writeGeneratorConfig(id=k)
                time.sleep(0.1)
            if ctrlmode:                
                self.driver.writeControlConfig()
                self.driver.setAlgOn(False, 0, forcewrite=True)
                self.driver.startControl()
            else:             
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
                    for j in range(3):
                        if self.driver.IMUEnableFlags[j]:
                            for k in range(3):
                                self.accdata[j][k][self.globalctreadings] = self.driver.accreadings[j][k]
                                self.gyrodata[j][k][self.globalctreadings] = self.driver.gyroreadings[j][k]
                self.dacoutdata[0][self.globalctreadings] = self.driver.dacout[0]
                self.dacoutdata[1][self.globalctreadings] = self.driver.dacout[1]
                self.dacoutdata[2][self.globalctreadings] = self.driver.dacout[2]
                self.dacoutdata[3][self.globalctreadings] = self.driver.dacout[3]
                for k in range(4):
                    if self.driver.adcenablemap[k] != 0:
                        self.adcdata[k][self.globalctreadings] = self.driver.adcin[k]
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
        self.mwindow.ui.sampleTime.setText(f'{self.driver.calctime:.0f} us')
        if self.driver.controlMode:
            self.ctrlfig.updateFig()
        else:
            self.mfig.updateFig()
        self.ofig.updateFig()
        # application.ui.progressBar.setValue(self.globalctreadings // 2000)

    def ResetaDados(self):
        self.maxv = 1000
        self.flagsaved = True
        self.globalctreadings = 0        
        self.mwindow.ui.elapsedTime.setText('0 s')
        self.mwindow.ui.controlTime.setText('0 s')
        self.mwindow.ui.sampleTime.setText('0 us')
        self.accdata = [[np.zeros(self.wsize), np.zeros(self.wsize), np.zeros(self.wsize)],
                        [np.zeros(self.wsize), np.zeros(self.wsize), np.zeros(self.wsize)],
                        [np.zeros(self.wsize), np.zeros(self.wsize), np.zeros(self.wsize)]]
        self.gyrodata = [[np.zeros(self.wsize), np.zeros(self.wsize), np.zeros(self.wsize)],
                        [np.zeros(self.wsize), np.zeros(self.wsize), np.zeros(self.wsize)],
                        [np.zeros(self.wsize), np.zeros(self.wsize), np.zeros(self.wsize)]]
        self.dacoutdata = [np.zeros(self.wsize), np.zeros(self.wsize), np.zeros(self.wsize), np.zeros(self.wsize)]
        self.adcdata = [np.zeros(self.wsize), np.zeros(self.wsize), np.zeros(self.wsize), np.zeros(self.wsize)]
        self.xrefdata = np.zeros(self.wsize)
        self.xerrodata = np.zeros(self.wsize)
        self.mfig.updateFig(self.driver.controlMode, [self.driver.refid, self.driver.erroid])
        self.ofig.updateFig()
        self.ctrlfig.updateFig()
        

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
            thedict = {
                "Tempo (s)": self.timereads[0:limf],                
                "DAC 1": self.dacoutdata[0][0:limf],
                "DAC 2": self.dacoutdata[1][0:limf],
                "DAC 3": self.dacoutdata[2][0:limf],
                "DAC 4": self.dacoutdata[3][0:limf],
                "ADC 1": self.adcdata[0][0:limf],
                "ADC 2": self.adcdata[1][0:limf],
                "ADC 3": self.adcdata[2][0:limf],
                "ADC 4": self.adcdata[3][0:limf]
            }
            for k in range(3):
                if self.driver.IMUEnableFlags[k]:
                    thedict[f"IMU{k+1}AccX"] = self.accdata[k][0][0:limf]
                    thedict[f"IMU{k+1}AccY"] = self.accdata[k][1][0:limf]
                    thedict[f"IMU{k+1}AccZ"] = self.accdata[k][2][0:limf]
                    thedict[f"IMU{k+1}GyroX"] = self.gyrodata[k][0][0:limf]
                    thedict[f"IMU{k+1}GyroY"] = self.gyrodata[k][1][0:limf]
                    thedict[f"IMU{k+1}GyroZ"] = self.gyrodata[k][2][0:limf]
                    
            df = pd.DataFrame(thedict)            
            df.to_feather(filename)
            # df.to_csv(filename)

        self.flagsaved = setsaved
