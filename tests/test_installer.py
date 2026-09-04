import tempfile
import unittest
from pathlib import Path

from installer._common import write_version_file


class InstallerMetadataTests(unittest.TestCase):
    def test_version_info_is_a_single_eval_expression(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "version_info.txt"
            write_version_file(
                "1.2.3",
                output_path,
                description="ActVib",
                filename="ActVib.exe",
            )

            source = output_path.read_text(encoding="utf-8")
            compile(source, str(output_path), "eval")
            self.assertNotIn("import ", source)
