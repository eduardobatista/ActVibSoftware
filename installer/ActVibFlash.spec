# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for the ActVibFlash helper (Windows onedir build).

ActVibFlash is a minimal console-less wrapper around ``esptool.main()``,
invoked by ActVib/updater.py as a subprocess when the main application is
frozen. It is built independently from ActVib.exe so that the GPL-licensed
esptool dependency stays isolated in its own executable/process boundary,
matching the arrangement used in the regular ``uv``-installed distribution
(a separate ``esptool`` console-script).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(SPEC).resolve().parent))  # noqa: F821

from _common import PROJECT_ROOT, project_version, write_version_file  # noqa: E402
from PyInstaller.utils.hooks import copy_metadata  # noqa: E402

VERSION = project_version()
BUILD_DIR = Path(SPECPATH).resolve()  # noqa: F821
VERSION_FILE = write_version_file(
    VERSION,
    BUILD_DIR / "ActVibFlash_version_info.txt",
    description="ActVib Firmware Flasher",
    filename="ActVibFlash.exe",
)

datas = copy_metadata("esptool")

a = Analysis(  # noqa: F821
    [str(PROJECT_ROOT / "installer" / "flasher_main.py")],
    pathex=[str(PROJECT_ROOT)],
    binaries=[],
    datas=datas,
    hiddenimports=["esptool", "esptool.targets", "serial"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)  # noqa: F821

exe = EXE(  # noqa: F821
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="ActVibFlash",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version=str(VERSION_FILE),
    uac_admin=False,
)
