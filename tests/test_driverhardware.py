import unittest

import numpy as np

from ActVib.driverhardware import driverhardware


class FakeSerial:
    def __init__(self, responses):
        self.responses = list(responses)
        self.writes = []

    def write(self, data):
        self.writes.append(bytes(data))

    def read(self, _size):
        return self.responses.pop(0)


class FakeProgressBar:
    def __init__(self):
        self.maximum = None
        self.current = 0

    def setMaximum(self, maximum):
        self.maximum = maximum

    def setValue(self, value):
        self.current = value

    def value(self):
        return self.current


class PathUploadTests(unittest.TestCase):
    def test_path_is_sent_in_64_byte_packets(self):
        driver = object.__new__(driverhardware)
        driver.serial = FakeSerial((b"k", b"\x00\x10", b"\x00\x04"))
        progress = FakeProgressBar()
        values = np.arange(20, dtype=float)

        driver.gravaCaminho("s", values, progress)

        self.assertEqual(driver.serial.writes[0], b"Ws")
        self.assertEqual(driver.serial.writes[1], b"\x00\x50")
        self.assertEqual(len(driver.serial.writes[2]), 64)
        self.assertEqual(len(driver.serial.writes[3]), 16)
        self.assertEqual(progress.maximum, 80)
        self.assertEqual(progress.current, 80)

    def test_incomplete_device_response_fails_upload(self):
        driver = object.__new__(driverhardware)
        driver.serial = FakeSerial((b"k", b""))

        with self.assertRaisesRegex(RuntimeError, "Incomplete response"):
            driver.gravaCaminho(
                "s", np.arange(16, dtype=float), FakeProgressBar()
            )

    def test_path_larger_than_firmware_buffer_is_rejected(self):
        driver = object.__new__(driverhardware)
        driver.serial = FakeSerial(())

        with self.assertRaisesRegex(ValueError, "3000"):
            driver.gravaCaminho(
                "s", np.arange(3001, dtype=float), FakeProgressBar()
            )


if __name__ == "__main__":
    unittest.main()
