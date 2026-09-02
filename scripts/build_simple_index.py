import argparse
import hashlib
import html
import json
import os
import re
import urllib.parse
import urllib.request
from pathlib import Path

PACKAGE_NAME = "actvibsoftware"
REQUIRES_PYTHON = ">=3.13,<3.14"
DIST_PATTERN = re.compile(r"^actvibsoftware-.+\.(?:whl|tar\.gz)$", re.IGNORECASE)


def get_release_assets(repository, token=None):
    assets = {}
    page = 1
    while True:
        request = urllib.request.Request(
            f"https://api.github.com/repos/{repository}/releases?per_page=100&page={page}",
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": "ActVibSoftware-index-builder",
                **({"Authorization": f"Bearer {token}"} if token else {}),
            },
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            releases = json.load(response)
        for release in releases:
            if release.get("draft"):
                continue
            for asset in release.get("assets", []):
                filename = asset.get("name", "")
                if DIST_PATTERN.fullmatch(filename):
                    assets[filename] = (asset["browser_download_url"], None)
        if len(releases) < 100:
            break
        page += 1
    return assets


def add_local_distributions(assets, repository, tag, dist_directory):
    encoded_tag = urllib.parse.quote(tag, safe="")
    for distribution in Path(dist_directory).iterdir():
        if not distribution.is_file() or not DIST_PATTERN.fullmatch(distribution.name):
            continue
        encoded_name = urllib.parse.quote(distribution.name, safe="")
        url = (
            f"https://github.com/{repository}/releases/download/"
            f"{encoded_tag}/{encoded_name}"
        )
        digest = hashlib.sha256(distribution.read_bytes()).hexdigest()
        assets[distribution.name] = (url, digest)


def write_index(assets, output_directory):
    if not assets:
        raise RuntimeError("No ActVib distributions were found")

    output = Path(output_directory)
    package_directory = output / "simple" / PACKAGE_NAME
    package_directory.mkdir(parents=True, exist_ok=True)

    links = []
    requires_python = html.escape(REQUIRES_PYTHON, quote=True)
    for filename, (url, digest) in sorted(assets.items()):
        if digest:
            url = f"{url}#sha256={digest}"
        links.append(
            f"    <a data-requires-python=\"{requires_python}\" "
            f"href=\"{html.escape(url, quote=True)}\">"
            f"{html.escape(filename)}</a><br>"
        )

    package_html = "\n".join(
        [
            "<!doctype html>",
            '<html lang="en">',
            "  <head>",
            '    <meta charset="utf-8">',
            '    <meta name="pypi:repository-version" content="1.0">',
            "    <title>Links for actvibsoftware</title>",
            "  </head>",
            "  <body>",
            "    <h1>Links for actvibsoftware</h1>",
            *links,
            "  </body>",
            "</html>",
            "",
        ]
    )
    (package_directory / "index.html").write_text(package_html, encoding="utf-8")

    simple_directory = output / "simple"
    simple_html = """<!doctype html>
<html lang="en">
  <head><meta charset="utf-8"><title>ActVib package index</title></head>
  <body><a href="actvibsoftware/">actvibsoftware</a></body>
</html>
"""
    (simple_directory / "index.html").write_text(simple_html, encoding="utf-8")

    root_html = """<!doctype html>
<html lang="en">
  <head><meta charset="utf-8"><title>ActVib releases</title></head>
  <body>
    <h1>ActVib releases</h1>
    <p>This site hosts the <a href="simple/">ActVib Python package index</a>.</p>
  </body>
</html>
"""
    (output / "index.html").write_text(root_html, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Build the ActVib PEP 503 index")
    parser.add_argument("--repository", required=True, help="GitHub owner/repository")
    parser.add_argument("--tag", required=True, help="Current GitHub release tag")
    parser.add_argument("--dist", default="dist", help="Local distribution directory")
    parser.add_argument("--output", default="site", help="Output site directory")
    args = parser.parse_args()

    assets = get_release_assets(args.repository, os.environ.get("GITHUB_TOKEN"))
    add_local_distributions(assets, args.repository, args.tag, args.dist)
    write_index(assets, args.output)


if __name__ == "__main__":
    main()
