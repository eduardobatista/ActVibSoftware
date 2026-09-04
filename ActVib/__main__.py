import os
import sys

# In a Windows frozen build without a console (windowed mode), sys.stdout and
# sys.stderr are None. Some dependencies (or stray print() calls) assume they
# are always available, so provide harmless no-op streams before anything
# else runs. See PyInstaller docs: "sys.stdin, sys.stdout, and sys.stderr in
# noconsole/windowed applications (Windows only)".
if sys.stdout is None:
    sys.stdout = open(os.devnull, "w")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w")

import qdarktheme
from PySide6 import QtCore, QtWidgets
from PySide6.QtGui import QFont, QIcon

from .dataman import dataman
from .driverhardware import driverhardware
from .mainwindow import mainwindow

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("ActVib")
    app.setOrganizationName("ActVib")

    icon_path = os.path.join(ASSETS_DIR, "actvib.png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    qdarktheme.setup_theme("light")
    app.setFont(QFont("Fira Sans", 10))

    drv = driverhardware()
    dman = dataman(drv)
    window = mainwindow(app, drv, dman)
    window.show()

    if os.environ.get("ACTVIB_SMOKE_TEST") == "1":
        _run_smoke_checks()
        QtCore.QTimer.singleShot(0, app.quit)

    return app.exec()


def _run_smoke_checks():
    """Exercise a few dependencies that are easy to break when freezing the
    application (e.g. missing PyArrow engine, missing Qt plugins). Used only
    by the CI/packaging smoke test, gated by ACTVIB_SMOKE_TEST=1.
    """
    import tempfile

    import pandas as pd

    with tempfile.TemporaryDirectory(prefix="actvib-smoke-") as temp_dir:
        path = os.path.join(temp_dir, "smoke.feather")
        df = pd.DataFrame({"a": [1, 2, 3], "b": [4.0, 5.0, 6.0]})
        df.to_feather(path)
        pd.read_feather(path)


if __name__ == "__main__":
    raise SystemExit(main())
