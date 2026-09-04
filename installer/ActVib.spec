# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for the ActVib main application (Windows onedir build)."""

import sys
from pathlib import Path

# SPEC is injected by PyInstaller into the namespace this file is exec'd in.
sys.path.insert(0, str(Path(SPEC).resolve().parent))  # noqa: F821

from _common import PROJECT_ROOT, project_version, write_version_file  # noqa: E402
from PyInstaller.utils.hooks import copy_metadata  # noqa: E402

VERSION = project_version()
BUILD_DIR = Path(SPECPATH).resolve()  # noqa: F821
VERSION_FILE = write_version_file(
    VERSION,
    BUILD_DIR / "ActVib_version_info.txt",
    description="ActVib",
    filename="ActVib.exe",
)

datas = [
    (str(PROJECT_ROOT / "ActVib" / "assets" / "actvib.png"), "ActVib/assets"),
    (str(PROJECT_ROOT / "ActVib" / "assets" / "actvib.ico"), "ActVib/assets"),
    (str(PROJECT_ROOT / "LICENSE"), "."),
    (str(PROJECT_ROOT / "THIRD_PARTY_NOTICES.txt"), "."),
]
# Copy metadata so importlib.metadata.version("actvibsoftware") works when
# frozen (used by ActVib/updater.py to display the installed version).
datas += copy_metadata("actvibsoftware")

a = Analysis(  # noqa: F821
    [str(PROJECT_ROOT / "main.py")],
    pathex=[str(PROJECT_ROOT)],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["esptool", "espefuse", "espsecure", "esp_rfc2217_server"],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)  # noqa: F821

exe = EXE(  # noqa: F821
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="ActVib",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(PROJECT_ROOT / "ActVib" / "assets" / "actvib.ico"),
    version=str(VERSION_FILE),
    uac_admin=False,
    contents_directory=".",
)

coll = COLLECT(  # noqa: F821
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="ActVib",
)
