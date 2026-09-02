import hashlib
import tempfile
import unittest
from pathlib import Path

from scripts.build_simple_index import add_local_distributions, write_index


class SimpleIndexTests(unittest.TestCase):
    def test_local_distribution_is_published_with_hash(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            dist = root / "dist"
            dist.mkdir()
            wheel = dist / "actvibsoftware-0.9.0-py3-none-any.whl"
            wheel.write_bytes(b"wheel-content")
            assets = {}

            add_local_distributions(
                assets, "owner/ActVibSoftware", "v0.9.0", dist
            )
            write_index(assets, root / "site")

            package_index = (
                root / "site/simple/actvibsoftware/index.html"
            ).read_text(encoding="utf-8")
            self.assertIn(wheel.name, package_index)
            self.assertIn(hashlib.sha256(wheel.read_bytes()).hexdigest(), package_index)
            self.assertIn("data-requires-python=\"&gt;=3.13,&lt;3.14\"", package_index)


if __name__ == "__main__":
    unittest.main()
