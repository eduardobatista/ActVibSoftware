import hashlib
import hmac
import json
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
import zipfile
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path, PurePosixPath
from threading import Thread

from PySide6 import QtCore
from PySide6.QtWidgets import QDialog

from .UpdaterDialog import Ui_UpdaterDialog as UpdaterDialog


class Updater(QtCore.QObject):
    actionMessage = QtCore.Signal(str, bool)
    updateFinished = QtCore.Signal()

    SOFTWARE_RELEASES_URL = "https://github.com/eduardobatista/ActVibSoftware/releases"
    PACKAGE_INDEX_URL = "https://eduardobatista.github.io/ActVibSoftware/simple/"
    FIRMWARE_RELEASE_API = (
        "https://api.github.com/repos/eduardobatista/ActVibFirmware/releases/latest"
    )
    FIRMWARE_FALLBACK_URL = (
        "https://github.com/eduardobatista/ActVibFirmware/archive/refs/heads/beta.zip"
    )
    LEGACY_FIRMWARE_FILES = (
        ("0x1000", "ActVibFirmware.ino.bootloader.bin"),
        ("0x8000", "ActVibFirmware.ino.partitions.bin"),
        ("0xe000", "boot_app0.bin"),
        ("0x10000", "ActVibFirmware.ino.bin"),
    )

    def __init__(self, driver=None):
        super().__init__()
        self.driver = driver
        self.port = None
        self.seqthread = None
        self.flagrunning = False

        self.udialog = QDialog()
        self.udialog.ui = UpdaterDialog()
        self.udialog.ui.setupUi(self.udialog)
        self.udialog.ui.messageArea.setReadOnly(True)
        self.udialog.ui.startSoftware.setText("Show Software Update Instructions")
        self.udialog.ui.startFirmware.clicked.connect(self.startFWUpdate)
        self.udialog.ui.startSoftware.clicked.connect(self.startSWUpdate)
        self.updateFinished.connect(self._update_finished)

    def showUpdaterDialog(self, port):
        self.port = port
        self.udialog.ui.messageArea.clear()
        self.udialog.ui.startFirmware.setEnabled(bool(port) and not self.flagrunning)
        if not port:
            self.actionMessage.emit(
                "Select a serial port before updating the firmware.\n", False
            )
        self.udialog.exec()

    @QtCore.Slot(str, bool)
    def printMessage(self, msg, isHtml):
        if isHtml:
            self.udialog.ui.messageArea.insertHtml(msg)
        else:
            self.udialog.ui.messageArea.insertPlainText(msg)
        self.udialog.ui.messageArea.ensureCursorVisible()

    def startFWUpdate(self):
        self.udialog.ui.messageArea.clear()
        if not self.port:
            self.actionMessage.emit(
                "Select a serial port before updating the firmware.\n", False
            )
            return
        if self.flagrunning:
            return

        self.flagrunning = True
        self.udialog.ui.startFirmware.setEnabled(False)
        self.udialog.ui.startSoftware.setEnabled(False)
        self.seqthread = Thread(target=self._run_firmware_update, daemon=True)
        self.seqthread.start()

    def startSWUpdate(self):
        self.udialog.ui.messageArea.clear()
        if getattr(sys, "frozen", False):
            self.actionMessage.emit(
                "ActVib was installed with the Windows installer. Download the "
                "latest installer or portable ZIP from the Releases page below, "
                "close ActVib, and run the new installer (it will replace the "
                "current installation).\n\n"
                f"Releases: {self.SOFTWARE_RELEASES_URL}\n",
                False,
            )
            return

        try:
            installed_version = version("actvibsoftware")
        except PackageNotFoundError:
            installed_version = "development checkout"

        project_root = Path(__file__).resolve().parent.parent
        if (project_root / ".git").exists():
            command = "git pull\nuv sync --locked"
        else:
            command = (
                f"uv tool upgrade --index {self.PACKAGE_INDEX_URL} actvibsoftware"
            )
        self.actionMessage.emit(
            f"Installed version: {installed_version}\n\n"
            "Software updates are managed by uv. Close ActVib, open a terminal, "
            f"and run:\n\n{command}\n\n"
            f"Releases: {self.SOFTWARE_RELEASES_URL}\n",
            False,
        )

    def _run_firmware_update(self):
        try:
            if self.driver and self.driver.serial and self.driver.serial.is_open:
                self.actionMessage.emit("Closing the serial port...\n", False)
                self.driver.closeSerial()
                time.sleep(0.5)

            with tempfile.TemporaryDirectory(prefix="actvib-firmware-") as temp_dir:
                temp_path = Path(temp_dir)
                archive_path = temp_path / "firmware.zip"
                archive_url, release_name = self._firmware_archive_url()
                self.actionMessage.emit(
                    f"Downloading firmware ({release_name})...\n", False
                )
                self._download(archive_url, archive_path)
                plan, firmware_files, legacy = self._prepare_firmware(
                    archive_path, temp_path
                )
                if legacy:
                    self.actionMessage.emit(
                        "Warning: this legacy firmware package has no manifest or "
                        "published checksums.\n",
                        False,
                    )
                self.actionMessage.emit("Firmware files validated. Flashing...\n", False)
                self._flash(plan, firmware_files, temp_path)

            self.actionMessage.emit("\nFirmware update completed successfully.\n", False)
        except Exception as exc:  # noqa: BLE001 - report worker failures in the dialog
            self.actionMessage.emit(f"\nFirmware update failed: {exc}\n", False)
        finally:
            self.updateFinished.emit()

    def _firmware_archive_url(self):
        request = urllib.request.Request(
            self.FIRMWARE_RELEASE_API,
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": "ActVibSoftware",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=10) as response:
                release = json.load(response)
            zip_assets = [
                asset
                for asset in release.get("assets", [])
                if asset.get("name", "").lower().endswith(".zip")
                and "firmware" in asset.get("name", "").lower()
            ]
            if zip_assets:
                return zip_assets[0]["browser_download_url"], release.get(
                    "tag_name", "latest release"
                )
            if release.get("zipball_url"):
                return release["zipball_url"], release.get(
                    "tag_name", "latest release"
                )
        except (OSError, ValueError, KeyError, urllib.error.HTTPError):
            pass
        return self.FIRMWARE_FALLBACK_URL, "beta branch fallback"

    @staticmethod
    def _download(url, destination):
        request = urllib.request.Request(url, headers={"User-Agent": "ActVibSoftware"})
        with urllib.request.urlopen(request, timeout=60) as response:
            content_length = response.headers.get("Content-Length")
            if content_length and int(content_length) > 100 * 1024 * 1024:
                raise RuntimeError("Firmware archive is larger than 100 MB")
            with destination.open("wb") as output:
                downloaded = 0
                while chunk := response.read(1024 * 1024):
                    downloaded += len(chunk)
                    if downloaded > 100 * 1024 * 1024:
                        raise RuntimeError("Firmware archive is larger than 100 MB")
                    output.write(chunk)

    @classmethod
    def _prepare_firmware(cls, archive_path, temp_path):
        with zipfile.ZipFile(archive_path, "r") as archive:
            members = [info for info in archive.infolist() if not info.is_dir()]
            manifest_members = [
                info for info in members if PurePosixPath(info.filename).name == "manifest.json"
            ]
            if len(manifest_members) > 1:
                raise RuntimeError("Firmware archive contains multiple manifests")
            manifest_member = manifest_members[0] if manifest_members else None

            if manifest_member:
                if manifest_member.file_size > 1024 * 1024:
                    raise RuntimeError("Firmware manifest is larger than 1 MB")
                with archive.open(manifest_member) as manifest_file:
                    manifest = json.load(manifest_file)
                plan = cls._validate_manifest(manifest)
                file_specs = plan.pop("files")
                legacy = False
            else:
                plan = {
                    "chip": "esp32",
                    "baud": 460800,
                    "before": "default-reset",
                    "after": "hard-reset",
                }
                file_specs = [
                    {"offset": offset, "name": name}
                    for offset, name in cls.LEGACY_FIRMWARE_FILES
                ]
                legacy = True

            extracted = []
            for file_spec in file_specs:
                filename = PurePosixPath(
                    str(file_spec["name"]).replace("\\", "/")
                ).name
                candidates = [
                    info
                    for info in members
                    if PurePosixPath(info.filename).name == filename
                    and (not legacy or "update" in PurePosixPath(info.filename).parts)
                ]
                if not candidates:
                    raise RuntimeError(f"Firmware file not found: {filename}")
                if len(candidates) > 1:
                    raise RuntimeError(f"Firmware archive contains duplicate files: {filename}")
                member = candidates[0]
                if member.file_size > 32 * 1024 * 1024:
                    raise RuntimeError(f"Firmware file is larger than 32 MB: {filename}")

                destination = temp_path / filename
                with archive.open(member) as source, destination.open("wb") as output:
                    shutil.copyfileobj(source, output)

                expected_hash = file_spec.get("sha256")
                actual_hash = hashlib.sha256(destination.read_bytes()).hexdigest()
                if expected_hash and not hmac.compare_digest(
                    actual_hash.lower(), str(expected_hash).lower()
                ):
                    raise RuntimeError(f"Checksum mismatch for {filename}")
                extracted.append((file_spec["offset"], destination))

        return plan, extracted, legacy

    @staticmethod
    def _validate_manifest(manifest):
        if not isinstance(manifest, dict):
            raise TypeError("Invalid firmware manifest")
        if manifest.get("schema_version") != 1:
            raise RuntimeError("Unsupported firmware manifest schema")
        if manifest.get("chip") != "esp32":
            raise RuntimeError("The firmware manifest does not target ESP32")

        baud = int(manifest.get("baud", 460800))
        if not 9600 <= baud <= 3_000_000:
            raise RuntimeError("Invalid firmware baud rate")

        files = manifest.get("files")
        if not isinstance(files, list) or not files:
            raise RuntimeError("The firmware manifest contains no files")
        validated_files = []
        seen_names = set()
        seen_offsets = set()
        for item in files:
            try:
                offset_value = int(str(item["offset"]), 0)
                offset = hex(offset_value)
                name = PurePosixPath(str(item["name"]).replace("\\", "/")).name
                sha256 = str(item["sha256"])
            except (KeyError, TypeError, ValueError) as exc:
                raise RuntimeError("Invalid firmware file entry") from exc
            if name in {"", ".", ".."} or not 0 <= offset_value < 0x1000000:
                raise RuntimeError("Invalid firmware file entry")
            if len(sha256) != 64 or any(c not in "0123456789abcdefABCDEF" for c in sha256):
                raise RuntimeError(f"Invalid checksum for {name}")
            if name in seen_names or offset in seen_offsets:
                raise RuntimeError("Duplicate file or offset in firmware manifest")
            seen_names.add(name)
            seen_offsets.add(offset)
            validated_files.append(
                {"offset": offset, "name": name, "sha256": sha256}
            )

        before = manifest.get("before", "default-reset")
        after = manifest.get("after", "hard-reset")
        if before not in {"default-reset", "usb-reset", "no-reset", "no-reset-no-sync"}:
            raise RuntimeError("Invalid reset mode in firmware manifest")
        if after not in {
            "hard-reset",
            "soft-reset",
            "no-reset",
            "no-reset-stub",
            "watchdog-reset",
        }:
            raise RuntimeError("Invalid reset mode in firmware manifest")

        return {
            "chip": "esp32",
            "baud": baud,
            "before": before,
            "after": after,
            "files": validated_files,
        }

    @staticmethod
    def _flasher_command():
        """Return the base command used to invoke esptool.

        In a normal (non-frozen) installation, esptool is a regular Python
        dependency, so it is invoked as ``python -u -m esptool``. In a
        PyInstaller-frozen build there is no ``python`` executable available,
        so a small companion executable (built from a separate PyInstaller
        spec) that simply forwards its arguments to ``esptool.main()`` is
        bundled alongside the main application, under a ``flasher``
        subdirectory.
        """
        if getattr(sys, "frozen", False):
            flasher_name = "ActVibFlash.exe" if sys.platform == "win32" else "ActVibFlash"
            flasher_path = Path(sys.executable).resolve().parent / "flasher" / flasher_name
            if not flasher_path.exists():
                raise RuntimeError(
                    f"Firmware flasher helper not found at {flasher_path}. "
                    "Reinstall ActVib or report this issue."
                )
            return [str(flasher_path)]

        python = Path(sys.prefix) / (
            "Scripts/python.exe" if sys.platform == "win32" else "bin/python"
        )
        if not python.exists():
            python = Path(sys.executable)
        return [str(python), "-u", "-m", "esptool"]

    def _flash(self, plan, firmware_files, working_directory):
        arguments = [
            "--chip",
            plan["chip"],
            "--port",
            str(self.port),
            "--baud",
            str(plan["baud"]),
            "--before",
            plan["before"],
            "--after",
            plan["after"],
            "write-flash",
            "--compress",
            "--flash-mode",
            "dio",
            "--flash-freq",
            "80m",
            "--flash-size",
            "4MB",
        ]
        for offset, filename in firmware_files:
            arguments.extend((offset, str(filename)))

        process = subprocess.Popen(
            [*Updater._flasher_command(), *arguments],
            cwd=working_directory,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            creationflags=(
                subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            ),
        )
        if process.stdout:
            for line in process.stdout:
                self.actionMessage.emit(line, False)
        return_code = process.wait()
        if return_code != 0:
            raise RuntimeError(f"esptool exited with status {return_code}")

    @QtCore.Slot()
    def _update_finished(self):
        self.flagrunning = False
        self.udialog.ui.startFirmware.setEnabled(bool(self.port))
        self.udialog.ui.startSoftware.setEnabled(True)
