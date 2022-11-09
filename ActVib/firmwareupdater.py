from pathlib import Path
import urllib.request 
import zipfile
import subprocess
import shlex
from threading import Thread

from PySide2 import QtCore
from PySide2.QtWidgets import QDialog

from .UpdaterDialog import Ui_UpdaterDialog as UpdaterDialog

class FirmwareUpdater(QtCore.QObject):

    actionMessage = QtCore.Signal((str,bool)) # message,isHtml

    def __init__(self):
        super().__init__()
        self.seqthread = None
        self.flagrunning = False
        self.zipurl = "https://github.com/eduardobatista/ActVibFirmware/archive/refs/heads/beta.zip" 
        self.udialog = QDialog()
        self.udialog.ui = UpdaterDialog()
        # self.pasteshortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+V"), self.adialog, self.catchPaste)
        self.udialog.ui.setupUi(self.udialog)
        self.udialog.ui.startFirmware.clicked.connect(self.startUpdate)       
    
    def showUpdaterDialog(self,port):
        self.port = port
        self.udialog.ui.messageArea.clear()                 
        self.udialog.exec_()

    def printMessage(self,msg,isHtml):
        if isHtml:
            self.udialog.ui.messageArea.insertHtml(msg)
        else:
            self.udialog.ui.messageArea.insertPlainText(msg)
        self.udialog.ui.messageArea.ensureCursorVisible()

    def startUpdate(self):        
        self.udialog.ui.messageArea.clear()
        self.seqthread = Thread(target=self.runUpdate)
        self.seqthread.start()
        self.flagrunning = True

    def runUpdate(self):
        try:
            tmpdir = Path.home() / ".actvibtemp"
            tmpdir.mkdir(parents=True,exist_ok=True)
            filestoremove = []
            self.actionMessage.emit("Tempdir created.<br>Downloading file...<br>",True)
            dfile = tmpdir / "downloadedfile.zip"
            urllib.request.urlretrieve(self.zipurl, dfile)
            self.actionMessage.emit("File downloaded.<br>Extracting...<br>",True)
            filestoremove.append(dfile)
            flashcmd = None
            with zipfile.ZipFile(dfile,"r") as zipref:
                for ff in zipref.namelist():
                    if "update" in ff:
                        zipref.extract(ff,tmpdir)
                        if "flashcommand.sh" in ff:
                            flashcmd = tmpdir / ff
                        filestoremove.append(tmpdir / ff)
            self.actionMessage.emit("Files extracted.<br>Flashing...<br>",True)
            if flashcmd:
                with open(flashcmd,"r") as ff:
                    fcmd = shlex.split(ff.read().replace("<SERIALPORT>",self.port))
                    self.actionMessage.emit(f'<br><strong>Running command:</strong> {(fcmd)} <br>',True)
                    self.actionMessage.emit(f'<br><span style="color: red;"><strong>WARNING: If connection fails, press and hold the "BOOT" button at the ESP32 board when trying to connect.</strong></span><br><br>',True)
                    try:
                        proc =  subprocess.Popen([fcmd[0],"--version"],stdout=subprocess.PIPE,cwd=flashcmd.parent)
                    except BaseException as ex:
                        fcmd[0] = "python"
                    proc =  subprocess.Popen(fcmd,stdout=subprocess.PIPE,cwd=flashcmd.parent)
                    while True:
                        # line = proc.stdout.readline().decode()
                        line = proc.stdout.read(1).decode()
                        self.actionMessage.emit(line,False)
                        if not line:
                            break
            self.actionMessage.emit("<br>Cleaning up...<br>",True)
            for fff in filestoremove:
                if not fff.is_dir():
                    fff.unlink()
            for par in flashcmd.parents:
                if par == tmpdir:
                    break
                else: 
                    par.rmdir()
            tmpdir.rmdir()
            self.actionMessage.emit("<strong>Finished!</strong>",True)
        except BaseException as ex:
            self.actionMessage.emit(f'<br><br><span style="color: red;"><strong>Error!</strong></span><br>{str(ex)}',True)
        self.flagrunning = False    
