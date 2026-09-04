import hashlib
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from ActVib.updater import Updater


class FirmwareArchiveTests(unittest.TestCase):
    def test_manifest_package_is_extracted_and_verified(self):
        payloads = {
            "bootloader.bin": b"bootloader",
            "firmware.bin": b"firmware",
        }
        manifest = {
            "schema_version": 1,
            "chip": "esp32",
            "baud": 460800,
            "files": [
                {
                    "offset": offset,
                    "name": name,
                    "sha256": hashlib.sha256(payload).hexdigest(),
                }
                for offset, (name, payload) in zip(
                    ("0x1000", "0x10000"), payloads.items()
                )
            ],
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            archive_path = temp_path / "firmware.zip"
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("manifest.json", json.dumps(manifest))
                for name, payload in payloads.items():
                    archive.writestr(f"firmware/{name}", payload)

            plan, files, legacy = Updater._prepare_firmware(archive_path, temp_path)

            self.assertFalse(legacy)
            self.assertEqual(plan["chip"], "esp32")
            self.assertEqual([offset for offset, _ in files], ["0x1000", "0x10000"])
            self.assertEqual(
                [path.read_bytes() for _, path in files], list(payloads.values())
            )

    def test_checksum_mismatch_is_rejected(self):
        manifest = {
            "schema_version": 1,
            "chip": "esp32",
            "files": [
                {
                    "offset": "0x10000",
                    "name": "firmware.bin",
                    "sha256": "0" * 64,
                }
            ],
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            archive_path = temp_path / "firmware.zip"
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("update/manifest.json", json.dumps(manifest))
                archive.writestr("update/firmware.bin", b"not-the-expected-content")

            with self.assertRaisesRegex(RuntimeError, "Checksum mismatch"):
                Updater._prepare_firmware(archive_path, temp_path)

    def test_legacy_beta_package_remains_supported(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            archive_path = temp_path / "firmware.zip"
            with zipfile.ZipFile(archive_path, "w") as archive:
                for _, name in Updater.LEGACY_FIRMWARE_FILES:
                    archive.writestr(f"ActVibFirmware-beta/update/{name}", name.encode())

            plan, files, legacy = Updater._prepare_firmware(archive_path, temp_path)

            self.assertTrue(legacy)
            self.assertEqual(plan["baud"], 460800)
            self.assertEqual(
                [(offset, path.name) for offset, path in files],
                list(Updater.LEGACY_FIRMWARE_FILES),
            )

    def test_esptool_command_matches_esp32_flash_layout(self):
        process = mock.Mock(stdout=None)
        process.wait.return_value = 0
        updater = SimpleNamespace(port="SERIAL_PORT")
        plan = {
            "chip": "esp32",
            "baud": 460800,
            "before": "default-reset",
            "after": "hard-reset",
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            firmware = Path(temp_dir) / "firmware.bin"
            with mock.patch(
                "ActVib.updater.subprocess.Popen", return_value=process
            ) as popen:
                Updater._flash(
                    updater, plan, [("0x10000", firmware)], Path(temp_dir)
                )

        command = popen.call_args.args[0]
        self.assertIn("esptool", command)
        self.assertIn("dio", command)
        self.assertIn("80m", command)
        self.assertIn("4MB", command)
        self.assertEqual(command[-2:], ["0x10000", str(firmware)])
        self.assertNotIn("shell", popen.call_args.kwargs)

    def test_esptool_command_uses_flasher_helper_when_frozen(self):
        process = mock.Mock(stdout=None)
        process.wait.return_value = 0
        updater = SimpleNamespace(port="SERIAL_PORT")
        plan = {
            "chip": "esp32",
            "baud": 460800,
            "before": "default-reset",
            "after": "hard-reset",
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            firmware = Path(temp_dir) / "firmware.bin"
            fake_root = Path(temp_dir) / "install"
            flasher_dir = fake_root / "flasher"
            flasher_dir.mkdir(parents=True)
            flasher_name = "ActVibFlash.exe" if sys.platform == "win32" else "ActVibFlash"
            flasher_path = flasher_dir / flasher_name
            flasher_path.write_text("")
            fake_exe = fake_root / (
                "ActVib.exe" if sys.platform == "win32" else "ActVib"
            )

            with mock.patch("ActVib.updater.sys.frozen", True, create=True), \
                mock.patch("ActVib.updater.sys.executable", str(fake_exe)), \
                mock.patch(
                    "ActVib.updater.subprocess.Popen", return_value=process
                ) as popen:
                Updater._flash(
                    updater, plan, [("0x10000", firmware)], Path(temp_dir)
                )

        command = popen.call_args.args[0]
        self.assertEqual(command[0], str(flasher_path.resolve()))
        self.assertNotIn("-m", command)
        self.assertEqual(command[-2:], ["0x10000", str(firmware)])

    def test_flasher_command_raises_when_helper_missing(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            fake_exe = Path(temp_dir) / "install" / (
                "ActVib.exe" if sys.platform == "win32" else "ActVib"
            )
            fake_exe.parent.mkdir(parents=True)
            with mock.patch("ActVib.updater.sys.frozen", True, create=True), \
                mock.patch("ActVib.updater.sys.executable", str(fake_exe)):
                with self.assertRaisesRegex(RuntimeError, "flasher helper not found"):
                    Updater._flasher_command()


if __name__ == "__main__":
    unittest.main()
