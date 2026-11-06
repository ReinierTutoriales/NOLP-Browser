#!/usr/bin/env python3
"""Apply or check a minimal NOLP stylesheet import in a pinned Firefox source tree.

No Gecko internals are replaced. Abort on unexpected upstream structure.
"""
import argparse
from pathlib import Path
import sys

IMPORT = '@import url("chrome://browser/skin/nolp-chrome.css");'\nJAR_ENTRY = '  skin/classic/browser/nolp-chrome.css                        (../shared/nolp-chrome.css)'\nJAR_PATH = Path('browser/themes/shared/jar.inc.mn')
TARGET = Path("browser/themes/shared/browser-shared.css")
SOURCE = Path(__file__).resolve().parents[1] / "integrations/firefox-chrome/nolp-chrome.css"

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--firefox-dir", required=True, type=Path)
    p.add_argument("--check", action="store_true")
    args = p.parse_args()
    root = args.firefox_dir.resolve()
    target = root / TARGET
    if not (root / "mach").is_file() or not target.is_file():
        p.error("Expected Firefox source tree with mach and browser-shared.css")
    data = target.read_text(encoding="utf-8")
    if not data.strip() or "browser" not in data.lower():
        p.error("Unexpected Firefox chrome stylesheet; manual upstream review required")
    dest = target.parent / "nolp-chrome.css"\n    jar = root / JAR_PATH\n    if not jar.is_file() or "skin/classic/browser/browser-shared.css" not in jar.read_text(encoding="utf-8"):\n        p.error("Firefox chrome packaging manifest changed; review required")\n    manifest = jar.read_text(encoding="utf-8")
    if args.check:
        if data.count(IMPORT) != 1 or manifest.count(JAR_ENTRY) != 1 or not dest.is_file() or dest.read_bytes() != SOURCE.read_bytes():
            p.error("NOLP overlay missing or differs from source")
        print("NOLP Firefox chrome overlay verified")
        return
    if manifest.count(JAR_ENTRY) > 1:\n        p.error("Duplicate NOLP chrome packaging entries")\n    if data.count(IMPORT) > 1:
        p.error("Duplicate NOLP imports")
    if dest.exists() and dest.read_bytes() != SOURCE.read_bytes():
        p.error("Existing NOLP overlay differs; review before overwriting")
    if IMPORT not in data:
        target.write_text(IMPORT + "\n" + data, encoding="utf-8")
    dest.write_bytes(SOURCE.read_bytes())
    print("NOLP chrome overlay applied; Firefox build/runtime validation still required")

if __name__ == "__main__":
    main()
