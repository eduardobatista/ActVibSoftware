import os
import sys

from PySide2 import QtWidgets

from .mainwindow import mainwindow
from .driverhardware import driverhardware
from .dataman import dataman

app = QtWidgets.QApplication([])
app.setStyle('Fusion')

mwindow = mainwindow(app)
driver = driverhardware(mwindow)
dman = dataman(driver, mwindow)
mwindow.setDriver(driver)
mwindow.setDataMan(dman)

mwindow.show()

sys.exit(app.exec_())
