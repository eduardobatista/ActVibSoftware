"""
Helper classes/methods
"""

import numpy as np
import pyqtgraph as pg

from .BaseFigQtGraph import BaseFigQtGraph

class CtrlFigQtGraph(BaseFigQtGraph):

    def __init__(self, dman, app):
        self.dman = dman
        self.app = app
        super().__init__(2, self.dman.samplingperiod)
        pens = [pg.mkPen('r', width=1), pg.mkPen('b', width=1)]
        self.lineref = self.pitens[0].plot(np.array([]), np.array([]), pen=pens[0])
        self.lineerr = self.pitens[1].plot(np.array([]), np.array([]), pen=pens[1])
        self.plotSetup()

    def plotSetup(self, sensorids=[0, 6]):
        for k in range(2):
            self.pitens[k].disableAutoRange()
            self.pitens[k].setLabel('bottom', 'Time (s)')
            if (sensorids[k] % 6) < 3:
                self.pitens[k].setLabel('left', f'{"Reference" if k == 0 else "Error"}<br>Acceleration (m/s²)')
                # self.miny[k] = -0.25
                # self.maxy[k] = 0.25
            else:
                self.pitens[k].setLabel('left', f'{"Reference" if k == 0 else "Error"}<br>Gyro (dg/s)')
                # self.miny[k] = -10
                # self.maxy[k] = 10
            self.pitens[k].setXRange(-self.janelax[k], 0, padding=0.01)
            self.pitens[k].setYRange(self.miny[k], self.maxy[k], padding=0.01)

    def updateFig(self):
        limi = [0, 0]
        limf = [0, 0]
        npontos = [0, 0]
        for k in range(2):
            limi[k] = self.dman.globalctreadings - self.npontosjanela[k]
            limf[k] = self.dman.globalctreadings
            if limi[k] < 0:
                limi[k] = 0
                npontos[k] = limf[k] - limi[k]
            else:
                npontos[k] = self.npontosjanela[k]
        if npontos[0] > 0:
            self.lineref.setData(self.vetoreixox[0][-npontos[0]:], self.dman.xrefdata[limi[0]:limf[0]])
            self.lineerr.setData(self.vetoreixox[1][-npontos[1]:], self.dman.xerrodata[limi[1]:limf[1]])
        else:
            self.lineref.setData([], [])
            self.lineerr.setData([], [])


class MyFigQtGraph(BaseFigQtGraph):

    def __init__(self, dman): # , app):
        self.dman = dman
        # self.app = app
        super().__init__(3, self.dman.samplingperiod)
        self.wsize = 60
        pens = [pg.mkPen('r', width=1), pg.mkPen('b', width=1), pg.mkPen('g', width=1), pg.mkPen('y', width=1)]
        self.lineacc = []
        self.linegyr = []        
        for k in range(3):
            self.lineacc.append(self.pitens[0].plot(np.array([]), np.array([]), pen=pens[k]))
            self.linegyr.append(self.pitens[1].plot(np.array([]), np.array([]), pen=pens[k]))
        self.lineadc = []
        for k in range(4):
            self.lineadc.append(self.pitens[2].plot(np.array([]), np.array([]), pen=pens[k]))
        for k, pitem in enumerate(self.pitens):
            pitem.disableAutoRange()
            pitem.setXRange(-self.janelax[k], 0, padding=0.01)
            pitem.setYRange(self.miny[k], self.maxy[k], padding=0.01)
            pitem.setLabel('bottom', 'Time (s)')
        self.pitens[0].setLabel('left', 'Accel. (m/s²)')
        self.pitens[1].setLabel('left', 'Gyro (dg/s)')
        self.pitens[2].setLabel('left', 'ADC (Volts)')
        self.accEnable = [True, True, True]
        self.gyroEnable = [True, True, True]
        self.adcEnableMap = [False, False, False, False]
        self.plotchoice = [0, 0]

    def setPlotChoice(self, idx1, idx2):
        if idx1 is not None:
            self.plotchoice[0] = idx1
        if idx2 is not None:
            self.plotchoice[1] = idx2
        
    def removeADCPlot(self):
        if self.getItem(2,0) is not None:
            self.removeItem(self.pitens[2])

    def addADCPlot(self):
        if self.getItem(2,0) is None:
            self.addItem(self.pitens[2],row=2,col=0)

    def updateFig(self, ctrlmode=False, sensorids=[0, 6]):
        limi = [0, 0, 0]
        limf = [0, 0, 0]
        npontos = [0, 0, 0]
        for k in range(3):
            limi[k] = self.dman.globalctreadings - self.npontosjanela[k]
            limf[k] = self.dman.globalctreadings
            if limi[k] < 0:
                limi[k] = 0
                npontos[k] = limf[k] - limi[k]
            else:
                npontos[k] = self.npontosjanela[k]
        for k in range(3):
            if self.accEnable[k] and (npontos[0] > 0):
                self.lineacc[k].setData(self.vetoreixox[0][-npontos[0]:], self.dman.accdata[self.plotchoice[0]][k][limi[0]:limf[0]])
            else:
                self.lineacc[k].setData([], [])
            if self.gyroEnable[k] and (npontos[1] > 0):
                self.linegyr[k].setData(self.vetoreixox[1][-npontos[1]:], self.dman.gyrodata[self.plotchoice[1]][k][limi[1]:limf[1]])
            else:
                self.linegyr[k].setData([], [])
        for k in range(4):
            if self.adcEnableMap[k] and (npontos[2] > 0):
                self.lineadc[k].setData(self.vetoreixox[2][-npontos[2]:],self.dman.adcdata[k][limi[2]:limf[2]])
            else:
                self.lineadc[k].setData([], [])
            


class FigOutputQtGraph(BaseFigQtGraph):

    def __init__(self, dman, app):
        self.dman = dman
        self.app = app
        super().__init__(1, self.dman.samplingperiod)
        self.pitem = self.pitens[0]
        pens = [pg.mkPen('r', width=1), pg.mkPen('b', width=1), pg.mkPen('g', width=1), pg.mkPen('y', width=1)]
        self.lines = []
        for k in range(4):
            self.lines.append(self.pitem.plot(np.array([]), np.array([]), pen=pens[k]))
            self.lines[k].setAlpha(0.5, False)
        self.pitem.disableAutoRange()
        self.pitem.setXRange(-self.janelax[0], 0, padding=0.01)
        self.pitem.setYRange(self.miny[0], self.maxy[0], padding=0.01)
        self.pitem.setLabel('bottom', 'Time (s)')
        self.pitem.setLabel('left', 'Normalized output')
        self.oldctr = 0
        self.dacenable = [True, False, False, False]

    def updateFig(self):

        limi = self.dman.globalctreadings - self.npontosjanela[0]
        limf = self.dman.globalctreadings

        if limi < 0:
            limi = 0
            npontos = limf - limi
        else:
            npontos = self.npontosjanela[0]

        if self.dman.ctrlmode:
            for k in range(2):
                if (npontos > 0):
                    self.lines[k].setData(self.vetoreixox[0][-npontos:], self.dman.dacoutdata[k][limi:limf])
                else:
                    self.lines[k].setData([], [])
            self.lines[2].setData([], [])
            self.lines[3].setData([], [])
        else:
            for k in range(4):
                if self.dacenable[k] and (npontos > 0):
                    self.lines[k].setData(self.vetoreixox[0][-npontos:], self.dman.dacoutdata[k][limi:limf])
                else:
                    self.lines[k].setData([], [])
