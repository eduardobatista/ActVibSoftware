"""Shared helpers for the PyInstaller spec files in this directory.

Spec files are executed as plain Python code by PyInstaller, but the
directory that contains them is not automatically added to ``sys.path``.
Each spec file adds it explicitly (using the ``SPEC`` global that PyInstaller
injects) before importing this module. See:
https://pyinstaller.org/en/stable/spec-files.html#using-shared-code-and-configuration-in-spec-files
"""

import tomllib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def project_version() -> str:
    with open(PROJECT_ROOT / "pyproject.toml", "rb") as pyproject_file:
        return tomllib.load(pyproject_file)["project"]["version"]


def windows_version_tuple(version: str) -> tuple[int, int, int, int]:
    """Convert a PEP 440-ish ``x.y.z`` version into a 4-number Windows tuple."""
    parts = version.split(".")[:3]
    numbers = [int("".join(ch for ch in part if ch.isdigit()) or "0") for part in parts]
    while len(numbers) < 3:
        numbers.append(0)
    return (numbers[0], numbers[1], numbers[2], 0)


def write_version_file(version: str, output_path: Path, *, description: str, filename: str) -> Path:
    """Write a PyInstaller version-info file (see ``pyi-grab_version`` format)."""
    file_version = windows_version_tuple(version)
    content = f'''# UTF-8
from PyInstaller.utils.win32.versioninfo import (
    FixedFileInfo,
    StringFileInfo,
    StringTable,
    StringStruct,
    VarFileInfo,
    VarStruct,
    VSVersionInfo,
)

VSVersionInfo(
  ffi=FixedFileInfo(
    filevers={file_version!r},
    prodvers={file_version!r},
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0),
  ),
  kids=[
    StringFileInfo(
      [
        StringTable(
          "040904B0",
          [
            StringStruct("CompanyName", "Eduardo Batista"),
            StringStruct("FileDescription", "{description}"),
            StringStruct("FileVersion", "{version}"),
            StringStruct("InternalName", "{filename}"),
            StringStruct("LegalCopyright", "Copyright (c) Eduardo Batista"),
            StringStruct("OriginalFilename", "{filename}"),
            StringStruct("ProductName", "ActVib"),
            StringStruct("ProductVersion", "{version}"),
          ],
        )
      ]
    ),
    VarFileInfo([VarStruct("Translation", [1033, 1200])]),
  ],
)
'''
    output_path.write_text(content, encoding="utf-8")
    return output_path
