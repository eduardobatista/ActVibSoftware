import json
import numpy as np

from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtWidgets import QMessageBox, QFileDialog, QDialog, QVBoxLayout

import pyqtgraph as pg
from pyqtgraph import PlotWidget, PlotItem, GraphicsWidget, GraphicsLayout, GraphicsLayoutWidget

class BaseFigQtGraph(GraphicsLayoutWidget):

    def __init__(self, nplots=1, samplingperiod=1):
        pg.setConfigOption("background", "w")
        pg.setConfigOption("foreground", "k")
        super().__init__()
        self.pitens = []
        for k in range(nplots):
            self.pitens.append(self.addPlot(row=k, col=0))
        for pi in self.pitens:
            pi.showAxis('top')
            pi.getAxis('top').setStyle(showValues=False)
            pi.showAxis('right')
            pi.getAxis('right').setStyle(showValues=False)
            pi.hideButtons()
            pi.setMouseEnabled(False, True)
            pi.setMenuEnabled(True, None)
            pi.setClipToView(True)            
        self.samplingperiod = samplingperiod
        self.janelax, self.miny, self.maxy, self.autoy, self.vetoreixox, self.npontosjanela = [], [], [], [], [], []
        for k in range(len(self.pitens)):
            self.janelax.append(5)
            self.miny.append(0)
            self.maxy.append(256)
            self.autoy.append(False)
            self.vetoreixox.append(0)
            self.npontosjanela.append(0)
        self.flagchangeranges = True
        for pi in self.pitens:
            pi.sigXRangeChanged.connect(self.sigXRangeChanged)
            pi.sigYRangeChanged.connect(self.sigYRangeChanged)

    def sizeHint(self):
        if self.parent() is None:
            return QtCore.QSize(30, 30)
        else:
            return QtCore.QSize(self.parent().frameGeometry().width(), self.parent().frameGeometry().height())

    def sigYRangeChanged(self):
        for k, pi in enumerate(self.pitens):
            rgs = pi.viewRange()
            if self.flagchangeranges:
                self.miny[k] = rgs[1][0]
                self.maxy[k] = rgs[1][1]

    def sigXRangeChanged(self):
        for k, pi in enumerate(self.pitens):
            if self.flagchangeranges:
                self.janelax[k] = round(-pi.viewRange()[0][0])
            self.npontosjanela[k] = int(self.janelax[k] / self.samplingperiod)
            self.vetoreixox[k] = np.linspace(-self.janelax[k], 0, self.npontosjanela[k])

    def setSamplingPeriod(self,newsampling):
        self.samplingperiod = newsampling
        self.sigXRangeChanged()

    def getConfigString(self):
        mvars = vars(self)
        d = {}
        for k in ('janelax', 'miny', 'maxy', 'autoy'):
            d[k] = mvars[k]
        return json.dumps(d)

    def parseConfigString(self, strdata):
        d = json.loads(strdata)
        ll = len(d['janelax'])
        self.janelax[0:ll] = d['janelax']
        self.miny[0:ll] = d['miny']
        self.maxy[0:ll] = d['maxy']
        self.autoy[0:ll] = d['autoy']
        self.flagchangeranges = False
        for k, pi in enumerate(self.pitens):
            self.pitens[k].setXRange(-self.janelax[k], 0.0, padding=0.01)
            self.pitens[k].setYRange(self.miny[k], self.maxy[k], padding=0.01)
        self.flagchangeranges = True
