import sys

from PySide6 import QtWidgets
from PySide6.QtGui import QFont

from .mainwindow import mainwindow
from .driverhardware import driverhardware
from .dataman import dataman
import qdarktheme

app = QtWidgets.QApplication([])

qdarktheme.setup_theme("light")

font = QFont("Fira Sans", 10)
app.setFont(font)

print(app.font())

drv = driverhardware()
dman = dataman(drv)

mwindow = mainwindow(app, drv, dman)

mwindow.show()

sys.exit(app.exec_())
