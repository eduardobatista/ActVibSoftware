import sys

from PySide6 import QtWidgets

from .mainwindow import mainwindow
from .driverhardware import driverhardware
from .dataman import dataman
from .figures import MyFigQtGraph
import qdarktheme


app = QtWidgets.QApplication([])

palette = qdarktheme.load_palette(theme="light")
stylesheet = qdarktheme.load_stylesheet(theme="dark")
app.setPalette(palette)

# qdarktheme.setup_theme("light")

# app.setStyleSheet(qdarktheme.load_stylesheet("light"))


drv = driverhardware()
dman = dataman(drv)
# mfig = MyFigQtGraph(dman, font=self.mainfont)

mwindow = mainwindow(app, drv, dman)

mwindow.show()

sys.exit(app.exec_())
