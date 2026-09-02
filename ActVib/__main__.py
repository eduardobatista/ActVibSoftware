import sys

import qdarktheme
from PySide6 import QtWidgets
from PySide6.QtGui import QFont

from .dataman import dataman
from .driverhardware import driverhardware
from .mainwindow import mainwindow


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("ActVib")
    app.setOrganizationName("ActVib")

    qdarktheme.setup_theme("light")
    app.setFont(QFont("Fira Sans", 10))

    drv = driverhardware()
    dman = dataman(drv)
    window = mainwindow(app, drv, dman)
    window.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
