"""
Helper classes/methods
"""
import os
from pathlib import Path

from PySide2 import (QtCore, QtWidgets)
from PySide2.QtWidgets import (QDialog, QFileDialog, QWidget)

import numpy as np
import pandas as pd
import pyqtgraph as pg

from .BaseFigQtGraph import BaseFigQtGraph
from .WorkdirDialog import Ui_Dialog as WorkdirDialog
from .UploadDialog import Ui_Dialog as UploadDialog


class WorkdirManager():

    def __init__(self, workdir):
        self.wdmandialog = QDialog()
        self.wdmandialog.ui = WorkdirDialog()
        self.wdmandialog.ui.setupUi(self.wdmandialog)
        self.workdir = workdir
        self.metafile = (Path(workdir) / 'metacontrol.feather')
        if self.metafile.exists():
            self.model = self.PandasModel(pd.read_feather(self.metafile))
            self.wdmandialog.ui.tableView.setModel(self.model)
            self.wdmandialog.ui.tableView.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
            self.wdmandialog.ui.bDelete.clicked.connect(self.delete)

    def showWorkdirManager(self):
        self.wdmandialog.exec_()

    def delete(self):
        selection = self.wdmandialog.ui.tableView.selectionModel().selectedRows()
        rows = []
        for ss in selection:
            rows.append(ss.row())
        metapath = Path(self.workdir) / 'metacontrol.feather'
        df = pd.read_feather(metapath)
        filestodelete = df.iloc[rows].filename.values
        for ff in filestodelete:
            fff = (Path(self.workdir) / ff)
            if fff.exists():
                fff.unlink()
        df = df.drop(rows)
        df = df.reset_index(drop=True)
        df.to_feather(metapath)
        self.model = self.PandasModel(df)
        self.wdmandialog.ui.tableView.setModel(self.model)

    class PandasModel(QtCore.QAbstractTableModel):
        """
        Class to populate a table view with a pandas dataframe
        """
        def __init__(self, data, parent=None):
            QtCore.QAbstractTableModel.__init__(self, parent)
            self._data = data

        def rowCount(self, parent=None):
            return len(self._data.values)

        def columnCount(self, parent=None):
            return self._data.columns.size

        def data(self, index, role=QtCore.Qt.DisplayRole):
            if index.isValid():
                if role == QtCore.Qt.DisplayRole:
                    return str(self._data.values[index.row()][index.column()])
            return None

        def headerData(self, col, orientation, role):
            if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
                return self._data.columns[col]
            return None


class MyUploadDialog():

    def __init__(self, driver):
        self.driver = driver
        self.uploaddialog = QDialog()
        self.uploaddialog.ui = UploadDialog()
        self.uploaddialog.ui.setupUi(self.uploaddialog)
        self.uploaddialog.ui.bAbre.clicked.connect(self.abreArquivo)
        self.uploaddialog.ui.progressBar.setValue(0)
        self.uploaddialog.ui.bGravar.clicked.connect(self.gravaDados)
        self.uploaddialog.ui.bGravaFlash.clicked.connect(self.gravaFlash)

    def showUploadDialog(self):
        self.uploaddialog.exec_()

    def abreArquivo(self):
        filename = QFileDialog.getOpenFileName(self.uploaddialog, "Abrir Arquivo",
                                               os.getenv('HOME'), 'feather (*.feather);;csv (*.csv)')
        if (filename[0] != ''):
            self.uploaddialog.ui.caminhoArquivo.setText(filename[0])
        else:
            self.uploaddialog.ui.caminhoArquivo.setText('')

    def gravaFlash(self):
        try:
            self.uploaddialog.ui.status.setText("")
            self.driver.openSerial()
            self.driver.handshake()
            self.driver.gravaFlash()
            self.uploaddialog.ui.status.setText("Gravação na flash concluída!")
            self.driver.stopReadings()
        except Exception as err:
            if self.driver.serial.isOpen():
                self.driver.stopReadings()
            self.uploaddialog.ui.status.setText(str(err))

    def gravaDados(self):
        try:
            self.uploaddialog.ui.status.setText("")
            fname = self.uploaddialog.ui.caminhoArquivo.text()
            if self.uploaddialog.ui.comboTipo.currentIndex() == 0:
                dataf = pd.read_feather(fname)
                if (dataf.columns[0] != 'wsec') or (dataf.columns[1] != 'wfbk'):
                    raise Exception("Dataframe inválida.")
                datasize = dataf.wsec.values.shape[0]
                if datasize > 3000:
                    raise Exception("Caminho com mais de 3000 amostras.")
                self.driver.openSerial()
                self.driver.handshake()
                self.driver.gravaCaminho('s', dataf.wsec.values, self.uploaddialog.ui.progressBar)
                self.driver.handshake()
                self.driver.gravaCaminho('f', dataf.wfbk.values, self.uploaddialog.ui.progressBar)
                self.uploaddialog.ui.status.setText("Gravação concluída!")
                self.driver.stopReadings()
            else:
                dataf = pd.read_csv(fname)
                datasize = dataf.values.shape[0]
                if datasize > 3000:
                    raise Exception("Caminho com mais de 3000 amostras.")
                datatitle = dataf.columns[0]
                if (datatitle == 'wsec') and (self.uploaddialog.ui.comboTipo.currentIndex() == 1):
                    tipo = 's'
                elif (datatitle == 'wfbk') and (self.uploaddialog.ui.comboTipo.currentIndex() == 2):
                    tipo = 'f'
                else:
                    raise Exception("Comb. título da coluna e dados incorreta.")
                self.driver.openSerial()
                self.driver.handshake()
                self.driver.gravaCaminho(tipo, dataf.values.reshape((1, -1))[0], self.uploaddialog.ui.progressBar)
                self.uploaddialog.ui.status.setText("Gravação concluída!")
                self.driver.stopReadings()
        except Exception as err:
            if self.driver.serial.isOpen():
                self.driver.stopReadings()
            self.uploaddialog.ui.status.setText(str(err))


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
            self.pitens[k].setLabel('bottom', 'Tempo (s)')
            if (sensorids[k] % 6) < 3:
                self.pitens[k].setLabel('left', 'Aceleração (m/s²)')
                # self.miny[k] = -0.25
                # self.maxy[k] = 0.25
            else:
                self.pitens[k].setLabel('left', 'Gyro (degrees/s)')
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

    def __init__(self, dman, app):
        self.dman = dman
        self.app = app
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
            pitem.setLabel('bottom', 'Tempo (s)')
        self.pitens[0].setLabel('left', 'Acceleration (m/s2)')
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
        self.pitem.setLabel('bottom', 'Tempo (s)')
        self.pitem.setLabel('left', 'Saída (normalizada)')
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

        for k in range(4):
            if self.dacenable[k] and (npontos > 0):
                self.lines[k].setData(self.vetoreixox[0][-npontos:], self.dman.dacoutdata[k][limi:limf])
            else:
                self.lines[k].setData([], [])

        # if self.dacenable[0] and (npontos > 0):
        #     self.lines[0].setData(self.vetoreixox[0][-npontos:], self.dman.dacoutdata[0][limi:limf])
        # else:
        #     self.lines[0].setData([], [])
        # if self.dacenable[1] and (npontos > 0):
        #     self.lines[1].setData(self.vetoreixox[0][-npontos:], self.dman.dacoutdata[1][limi:limf])
        # else:
        #     self.lines[1].setData([], [])
