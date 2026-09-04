"""Sanity checks for the frozen Windows ActVib bundle produced by
installer/build_windows.ps1. Run after building, before compiling the
installer, to fail fast with a clear message instead of a broken Setup.exe.

Usage (from repo root, on Windows):
    uv run python scripts/check_windows_bundle.py installer/dist/ActVib
"""

import sys
from pathlib import Path


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: check_windows_bundle.py <path-to-ActVib-onedir>")

    app_dir = Path(sys.argv[1]).resolve()
    if not app_dir.is_dir():
        raise RuntimeError(f"Not a directory: {app_dir}")

    checks = [
        ("main executable", app_dir / "ActVib.exe"),
        ("license file", app_dir / "LICENSE"),
        ("bundled icon", app_dir / "ActVib" / "assets" / "actvib.ico"),
        ("bundled icon (PNG)", app_dir / "ActVib" / "assets" / "actvib.png"),
        ("flasher helper", app_dir / "flasher" / "ActVibFlash.exe"),
        (
            "actvibsoftware package metadata",
            next(app_dir.glob("actvibsoftware-*.dist-info"), None) or Path("MISSING"),
        ),
    ]

    failures = []
    for label, path in checks:
        if not path.exists():
            failures.append(f"  - Missing {label}: {path}")
        else:
            print(f"OK: {label} -> {path}")

    if failures:
        raise RuntimeError("Windows bundle verification failed:\n" + "\n".join(failures))

    print("Windows bundle verification passed.")


if __name__ == "__main__":
    main()
