import os
import sys

from PySide2 import QtWidgets

from .mainwindow import mainwindow
from .driverhardware import driverhardware
from .dataman import dataman

app = QtWidgets.QApplication([])
app.setStyle('Fusion')

drv = driverhardware()
dman = dataman(drv)

mwindow = mainwindow(app, drv, dman)

mwindow.show()

sys.exit(app.exec_())
