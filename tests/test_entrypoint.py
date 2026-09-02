import os
import unittest
from unittest import mock

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6 import QtWidgets

from ActVib import __main__ as entrypoint


class EntrypointTests(unittest.TestCase):
    def test_main_window_starts_without_hardware(self):
        with mock.patch.object(QtWidgets.QApplication, "exec", return_value=0):
            self.assertEqual(entrypoint.main(), 0)


if __name__ == "__main__":
    unittest.main()
