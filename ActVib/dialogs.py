import os
from pathlib import Path

from PySide2 import (QtCore, QtWidgets)
from PySide2.QtWidgets import (QDialog, QFileDialog, QWidget)

import numpy as np
import pandas as pd
import pyqtgraph as pg

from .WorkdirDialog import Ui_Dialog as WorkdirDialog
from .UploadDialog import Ui_Dialog as UploadDialog
from .PathModeling import Ui_PathModelingDialog as PathModelingDialog
from .DSP import FIRNLMS,easyFourier

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



class MyPathModelingDialog():

    def __init__(self,dataman,driver):
        self.dataman = dataman
        self.driver = driver
        self.pdialog = QDialog()
        self.pdialog.ui = PathModelingDialog()
        self.pdialog.ui.setupUi(self.pdialog)
        self.endtime = np.ceil(self.dataman.timereads[self.dataman.globalctreadings-1])
        self.pdialog.ui.spinStartTime.setValue(0.0)
        # self.endtime = 200.0
        self.pdialog.ui.spinEndTime.setMaximum(self.endtime)
        self.pdialog.ui.spinEndTime.setValue(self.endtime)
        self.pdialog.ui.bRunModeling.clicked.connect(self.runModeling)
        self.gwidget = pg.GraphicsLayoutWidget()
        self.pdialog.ui.plotLayout.addWidget(self.gwidget)
        self.pdialog.ui.bOpenFile.clicked.connect(self.openFile)
        self.pdialog.ui.bUploadAndRec.setEnabled(False)
        self.pdialog.ui.bUploadAndRec.clicked.connect(self.recordData)
        self.pdialog.ui.progressBar.setValue(0)  
        self.pdialog.ui.bSaveToFile.clicked.connect(self.savePathsToFile)      
        self.datafromfile = None
        self.dataman.hasPaths = False
        
    def openFile(self):
        filename = QFileDialog.getOpenFileName(self.pdialog, "Open File",
                                               os.getenv('HOME'), 'feather (*.feather)')
        if (filename[0] != ''):
            self.pdialog.ui.fileName.setText(filename[0])
            self.datafromfile = pd.read_feather(filename[0])
            if "ctrl" not in self.datafromfile.columns:
                self.pdialog.ui.statusLabel.setText("File not valid (Error 1).")
                return
            self.endtime = self.datafromfile.time.values[-1]
            self.pdialog.ui.spinEndTime.setMaximum(self.endtime)
            self.pdialog.ui.spinEndTime.setValue(self.endtime)
            self.pdialog.ui.comboSource.setCurrentIndex(1)
        else:
            self.pdialog.ui.fileName.setText('')
            self.datafromfile = None

    def savePathsToFile(self):        
        if not self.dataman.hasPaths:
            self.pdialog.ui.statusLabel.setText("No paths in memory to be saved.")
            return
        else:
            self.pdialog.ui.statusLabel.setText("")
        filename = QFileDialog.getSaveFileName(self.pdialog, "Save File", os.getenv('HOME'), 'feather (*.feather)')
        if (filename[0] != ''):
            try:                
                dftosave = pd.DataFrame({
                    'wsec': self.dataman.secpath,
                    'wfbk': self.dataman.fbkpath
                })
                dftosave.to_feather(filename[0])
                self.pdialog.ui.statusLabel.setText("File saved successfully!")
            except Exception as err:
                self.pdialog.ui.statusLabel.setText(f"Error: {err}")

    def showPathModelingdDialog(self):
        self.pdialog.exec_()

    def recordData(self):
        self.pdialog.ui.statusLabel.setText("")
        try:                
            if self.dataman.hasPaths:
                    datasize = self.dataman.secpath.shape[0]
            else:
                raise Exception("Path data not found in memory.")
            self.driver.openSerial()
            self.driver.handshake()
            self.driver.gravaCaminho('s', self.dataman.secpath, self.pdialog.ui.progressBar)
            self.driver.handshake()
            self.driver.gravaCaminho('f', self.dataman.fbkpath, self.pdialog.ui.progressBar)
            self.driver.stopReadings()
            self.driver.openSerial()
            self.driver.handshake()
            self.driver.gravaFlash()
            self.pdialog.ui.statusLabel.setText("Successfully uploaded and written in flash!")
            self.driver.stopReadings()
        except BaseException as ex:
            self.pdialog.ui.statusLabel.setText(f"Error: {ex}")


    def runModeling(self):
        self.dataman.hasPaths = False

        psi = float(self.pdialog.ui.textPenalization.text())
        mu = float(self.pdialog.ui.textStepSize.text())
        N = self.pdialog.ui.spinMemSize.value()
        Navg = self.pdialog.ui.spinAveraging.value()
        endtime = self.pdialog.ui.spinEndTime.value()
        starttime = self.pdialog.ui.spinStartTime.value()

        try:

            if self.pdialog.ui.comboSource.currentIndex() == 0:
                if self.dataman.driver.controlMode and (not self.dataman.driver.taskIsControl) and (self.dataman.globalctreadings > 0):
                    limf = self.dataman.globalctreadings
                    timemask = (self.dataman.timereads[0:limf] >= starttime) & (self.dataman.timereads[0:limf] <= endtime)
                    x = self.dataman.dacoutdata[1][0:limf][timemask]
                    dfbk = self.dataman.xrefdata[0:limf][timemask]
                    dsec = self.dataman.xerrodata[0:limf][timemask]
                else:
                    raise BaseException("Path modeling recording not found")
            else:
                if self.datafromfile is not None:
                    timemask = (self.datafromfile.time >= starttime) & (self.datafromfile.time <= endtime)
                    x = self.datafromfile.ctrl[timemask].values
                    dfbk = self.datafromfile.ref[timemask].values            
                    dsec = self.datafromfile.err[timemask].values
                else:
                    raise BaseException("Path modeling recording not found (file not open)")
                

            dfbk = dfbk - np.mean(dfbk)
            dsec = dsec - np.mean(dsec)  

            filt = FIRNLMS(N,mu,psi,Navg)
            filt.run(x,dfbk)
            self.wfbk = filt.wwavg
            filt2 = FIRNLMS(N,mu,psi,Navg)
            filt2.run(x,dsec)
            self.wsec = filt2.wwavg

            pens = [pg.mkPen('r', width=1), pg.mkPen('b', width=1)]
            item = self.gwidget.getItem(0,0)
            if item is not None:
                self.gwidget.removeItem(item)
            item2 = self.gwidget.getItem(1,0)
            if item2 is not None:
                self.gwidget.removeItem(item2)
            myplot1 = self.gwidget.addPlot(row=0,col=0)
            myplot1.plot(self.wsec,pen=pens[0])
            myplot1.plot(self.wfbk,pen=pens[1])

            myplot2 = self.gwidget.addPlot(row=1,col=0)
            splfreq = (1/self.dataman.samplingperiod)
            magdb1,freqs1 = easyFourier(self.wsec,splfreq)
            myplot2.plot(freqs1,magdb1,pen=pens[0])
            magdb2,freqs2 = easyFourier(self.wfbk,splfreq)
            myplot2.plot(freqs2,magdb2,pen=pens[1])  

            self.dataman.hasPaths = True
            self.dataman.fbkpath = self.wfbk
            self.dataman.secpath = self.wsec

            self.pdialog.ui.statusLabel.setText(f"Success! Paths are available in memory for upload.")
            self.pdialog.ui.bUploadAndRec.setEnabled(True)

        except BaseException as ex:
            self.pdialog.ui.statusLabel.setText(f"Error: {ex}.")
        



class MyUploadDialog():

    def __init__(self, driver, dataman):
        self.driver = driver
        self.dataman = dataman
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
            self.uploaddialog.ui.status.setText("Successfully written in flash!")
            self.driver.stopReadings()
        except Exception as err:
            if self.driver.serial.isOpen():
                self.driver.stopReadings()
            self.uploaddialog.ui.status.setText(str(err))

    def gravaDados(self):
        try:
            self.uploaddialog.ui.status.setText("")
            fname = self.uploaddialog.ui.caminhoArquivo.text()
            if self.uploaddialog.ui.comboTipo.currentIndex() <= 2:
                if self.uploaddialog.ui.comboTipo.currentIndex() == 0:
                    dataf = pd.read_feather(fname)
                    if (dataf.columns[0] != 'wsec') or (dataf.columns[1] != 'wfbk'):
                        raise Exception("Invalid dataframe.")
                    datasize = dataf.wsec.values.shape[0]
                    if datasize > 3000:
                        raise Exception("Path having more than 3000 samples.")
                    wsec = dataf.wsec.values
                    wfbk = dataf.wfbk.values
                elif self.uploaddialog.ui.comboTipo.currentIndex() == 1:
                    if self.dataman.hasPaths:
                        wsec = self.dataman.secpath
                        wfbk = self.dataman.fbkpath  
                        datasize = wsec.shape[0]
                    else:
                        raise Exception("Path data not found in memory.")
                self.driver.openSerial()
                self.driver.handshake()
                self.driver.gravaCaminho('s', wsec, self.uploaddialog.ui.progressBar)
                self.driver.handshake()
                self.driver.gravaCaminho('f', wfbk, self.uploaddialog.ui.progressBar)
                self.uploaddialog.ui.status.setText("Upload finished!")
                self.driver.stopReadings()
            else:
                dataf = pd.read_csv(fname)
                datasize = dataf.values.shape[0]
                if datasize > 3000:
                    raise Exception("Path having more than 3000 samples.")
                datatitle = dataf.columns[0]
                if (datatitle == 'wsec') and (self.uploaddialog.ui.comboTipo.currentIndex() == 1):
                    tipo = 's'
                elif (datatitle == 'wfbk') and (self.uploaddialog.ui.comboTipo.currentIndex() == 2):
                    tipo = 'f'
                else:
                    raise Exception("Incorrect combination between column title and data.")
                self.driver.openSerial()
                self.driver.handshake()
                self.driver.gravaCaminho(tipo, dataf.values.reshape((1, -1))[0], self.uploaddialog.ui.progressBar)
                self.uploaddialog.ui.status.setText("Upload finished!")
                self.driver.stopReadings()
        except Exception as err:
            if self.driver.serial.isOpen():
                self.driver.stopReadings()
            self.uploaddialog.ui.status.setText(str(err))