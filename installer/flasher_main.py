"""Entry point for the standalone firmware-flashing helper (ActVibFlash).

This tiny executable exists only for Windows installer/portable builds of
ActVib, where the main application is a PyInstaller-frozen executable with no
usable ``python`` interpreter available on PATH or in ``sys.prefix``. Instead
of shipping a full Python environment, ActVib bundles this small companion
executable that simply forwards its command-line arguments to
``esptool.main()``.

It is built as an entirely separate PyInstaller bundle (see
``ActVibFlash.spec``) and placed by the installer/build script under a
``flasher`` subdirectory next to ``ActVib.exe``. See ``ActVib/updater.py``
(``Updater._flasher_command``) for the code that locates and invokes it.

This module is not part of the ``actvibsoftware`` wheel; it is only used when
building the Windows installer/portable bundle.
"""

import sys


def main():
    import esptool

    esptool.main(sys.argv[1:])


if __name__ == "__main__":
    raise SystemExit(main())
