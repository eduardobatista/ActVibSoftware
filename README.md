# ActVib

ActVib is a desktop application for monitoring, data acquisition, path modeling,
and active control of laboratory vibration experiments using an ESP32-based
controller.

## Requirements

- Windows 10/11 x64 or a current Linux distribution
- A USB port and an ActVib ESP32 controller
- Internet access during installation
- A CP210x or CH340/CH341 USB-to-serial driver

Python 3.13 and all Python dependencies are installed in an isolated environment
by [uv](https://docs.astral.sh/uv/). A separate system Python installation is not
required.

## Install On Windows

1. Install `uv` from an ordinary PowerShell window:

   ```powershell
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. Close and reopen PowerShell. If `uv` is still not found, run
   `uv tool update-shell` and reopen it again.
3. Install the USB driver for the bridge fitted to the controller:

   - [Silicon Labs CP210x VCP driver](https://www.silabs.com/developer-tools/usb-to-uart-bridge-vcp-drivers)
   - [WCH CH340/CH341 driver](https://www.wch-ic.com/downloads/CH341SER_EXE.html)

4. Disconnect and reconnect the controller after installing the driver.
5. Install ActVib:

   ```powershell
   uv tool install --python 3.13 --index https://eduardobatista.github.io/ActVibSoftware/simple/ actvibsoftware
   ```

6. Start the application:

   ```powershell
   actvib
   ```

Driver installers are not bundled with ActVib. Download them only from the
manufacturer links above.

## Install On Linux

CP210x and CH340/CH341 support is included in current Linux kernels. Install
`uv`, then install and start ActVib:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv tool install --python 3.13 --index https://eduardobatista.github.io/ActVibSoftware/simple/ actvibsoftware
actvib
```

If the serial port is visible but cannot be opened, identify its owning group:

```bash
ls -l /dev/ttyUSB0
```

Add your user to that group, then log out and back in. It is commonly `dialout`
on Debian/Ubuntu and `uucp` on Arch Linux:

```bash
sudo usermod -aG dialout "$USER"
# Arch Linux commonly uses:
sudo usermod -aG uucp "$USER"
```

Add only the group that owns the device on your system. Do not run ActVib as
root and do not make the serial device world-writable.

## Update Or Remove

Close ActVib before updating it:

```bash
uv tool upgrade --index https://eduardobatista.github.io/ActVibSoftware/simple/ actvibsoftware
```

Remove the application with:

```bash
uv tool uninstall actvibsoftware
```

The software-update button in ActVib displays these instructions instead of
overwriting installed source files.

## Firmware Update

The firmware is maintained separately in
[ActVibFirmware](https://github.com/eduardobatista/ActVibFirmware).

1. Connect the controller and select its port in **Setup > Port**.
2. Stop any active acquisition.
3. Open **Setup > Firmware Update** and start the firmware update.

ActVib downloads the ZIP asset from the latest firmware Release, validates its
manifest and SHA-256 checksums, closes the application serial connection, and
invokes its installed `esptool`. It never executes scripts from the downloaded
archive. Until the firmware repository publishes its first Release, the updater
uses the `beta` branch's `update` directory as a compatibility fallback and
warns that this legacy archive has no published checksums.

Firmware and software artifacts are intentionally unsigned. Manifest checksums
detect damaged or mismatched firmware files but do not authenticate the
publisher, so use only Releases from the official repositories linked here.

### Firmware Release Format

Attach a ZIP asset with `firmware` in its name to each ActVibFirmware GitHub
Release. The ZIP must contain one `manifest.json` and the files named by it.
File names must be unique within the ZIP.

```json
{
  "schema_version": 1,
  "chip": "esp32",
  "baud": 460800,
  "before": "default-reset",
  "after": "hard-reset",
  "files": [
    {
      "offset": "0x1000",
      "name": "ActVibFirmware.ino.bootloader.bin",
      "sha256": "0000000000000000000000000000000000000000000000000000000000000000"
    },
    {
      "offset": "0x8000",
      "name": "ActVibFirmware.ino.partitions.bin",
      "sha256": "0000000000000000000000000000000000000000000000000000000000000000"
    },
    {
      "offset": "0xe000",
      "name": "boot_app0.bin",
      "sha256": "0000000000000000000000000000000000000000000000000000000000000000"
    },
    {
      "offset": "0x10000",
      "name": "ActVibFirmware.ino.bin",
      "sha256": "0000000000000000000000000000000000000000000000000000000000000000"
    }
  ]
}
```

Replace every example checksum with the SHA-256 digest of the corresponding
binary before publishing the Release.

## Troubleshooting

- No port on Windows: check Device Manager, install the correct CP210x or
  CH340/CH341 driver, then reconnect the controller.
- Permission denied on Linux: add your user to the serial device's owning group
  and log in again.
- Port is busy: close serial monitors and other ActVib instances.
- Firmware flashing fails to connect: stop acquisition, verify the selected
  port, reconnect the controller, and retry. Some boards require holding the
  **BOOT** button while the connection starts.
- Installation cannot find `actvibsoftware`: verify that the repository's
  GitHub Pages deployment completed and that the `/simple/` URL is reachable.

## Development

```bash
git clone https://github.com/eduardobatista/ActVibSoftware.git
cd ActVibSoftware
uv sync --locked
uv run actvib
```

Run the automated checks and build the wheel and source distribution with:

```bash
QT_QPA_PLATFORM=offscreen uv run --locked python -m unittest discover -s tests -v
uv build
```

On Windows, set the headless Qt variable with
`$env:QT_QPA_PLATFORM = "offscreen"` before running the test command.

## Releases

Pushing a tag matching the version in `pyproject.toml` creates an unsigned
GitHub Release and deploys a PEP 503 package index to GitHub Pages:

```bash
git tag v0.9.0
git push origin v0.9.0
```

Configure **Settings > Pages > Source** as **GitHub Actions** before publishing
the first release.

## License

ActVib is available under the [MIT License](LICENSE).
