import hashlib
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from build_simple_index import write_index


def main():
    project_root = Path(__file__).resolve().parent.parent
    wheels = sorted((project_root / "dist").glob("actvibsoftware-*.whl"))
    if len(wheels) != 1:
        raise RuntimeError(f"Expected one wheel in dist, found {len(wheels)}")

    with tempfile.TemporaryDirectory(prefix="actvib-wheel-") as temp_dir:
        temp_path = Path(temp_dir)
        environment = temp_path / "venv"
        wheel = wheels[0].resolve()
        write_index(
            {
                wheel.name: (
                    wheel.as_uri(),
                    hashlib.sha256(wheel.read_bytes()).hexdigest(),
                )
            },
            temp_path / "site",
        )
        subprocess.run(
            ["uv", "venv", "--python", "3.13", str(environment)], check=True
        )
        python = environment / (
            "Scripts/python.exe" if sys.platform == "win32" else "bin/python"
        )
        subprocess.run(
            [
                "uv",
                "pip",
                "install",
                "--python",
                str(python),
                "--index",
                (temp_path / "site/simple").as_uri(),
                "actvibsoftware",
            ],
            check=True,
        )
        launcher = environment / (
            "Scripts/actvib.exe" if sys.platform == "win32" else "bin/actvib"
        )
        if not launcher.exists():
            raise RuntimeError("The wheel did not install the actvib launcher")
        environment_variables = {**os.environ, "QT_QPA_PLATFORM": "offscreen"}
        smoke_test = (
            "from importlib.metadata import version; "
            "from PySide6.QtWidgets import QApplication; "
            "from ActVib import __main__ as entrypoint; "
            "QApplication.exec = lambda self: 0; "
            "assert version('actvibsoftware'); "
            "assert entrypoint.main() == 0"
        )
        subprocess.run(
            [str(python), "-c", smoke_test],
            check=True,
            env=environment_variables,
        )


if __name__ == "__main__":
    main()
