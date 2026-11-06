#!/usr/bin/env python3
"""Install a minimal NOLP stylesheet into pinned Firefox Desktop chrome.

Only changes the known chrome stylesheet and jar manifest. Re-runnable and
fail-closed on unexpected upstream changes. Does not install a theme selector.
"""
import argparse
from pathlib import Path

IMPORT = '@import url("chrome://browser/skin/nolp-chrome.css");'
ANCHOR = '@import url("chrome://browser/skin/browser-colors.css");'
JAR_ENTRY = '  skin/classic/browser/nolp-chrome.css                        (../shared/nolp-chrome.css)'
JAR_ANCHOR = 'skin/classic/browser/browser-shared.css'
TARGET = Path("browser/themes/shared/browser-shared.css")
JAR_PATH = Path("browser/themes/shared/jar.inc.mn")
SOURCE = Path(__file__).resolve().parents[1] / "integrations/firefox-chrome/nolp-chrome.css"


def apply(root: Path, check: bool = False) -> None:
    root = root.resolve()
    target = root / TARGET
    jar = root / JAR_PATH
    dest = target.parent / "nolp-chrome.css"
    if not (root / "mach").is_file() or not target.is_file() or not jar.is_file():
        raise ValueError("Not a supported Firefox source tree")
    data = target.read_text(encoding="utf-8")
    manifest = jar.read_text(encoding="utf-8")
    if ANCHOR not in data or JAR_ANCHOR not in manifest:
        raise ValueError("Firefox upstream chrome layout changed; review required")
    if data.count(IMPORT) > 1 or manifest.count(JAR_ENTRY) > 1:
        raise ValueError("Duplicate NOLP chrome registration")
    if dest.exists() and dest.read_bytes() != SOURCE.read_bytes():
        raise ValueError("Existing NOLP stylesheet differs; manual review required")
    if check:
        if data.count(IMPORT) != 1 or manifest.count(JAR_ENTRY) != 1 or not dest.is_file():
            raise ValueError("NOLP chrome overlay is missing")
        return
    # Validate every input before modifying the upstream checkout.
    if IMPORT not in data:
        data = data.replace(ANCHOR, ANCHOR + "\n" + IMPORT, 1)
    if JAR_ENTRY not in manifest:
        manifest = manifest.rstrip("\n") + "\n" + JAR_ENTRY + "\n"
    target.write_text(data, encoding="utf-8")
    jar.write_text(manifest, encoding="utf-8")
    dest.write_bytes(SOURCE.read_bytes())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--firefox-dir", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        apply(args.firefox_dir, check=args.check)
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    print("NOLP Firefox chrome registration verified" if args.check else
          "NOLP Firefox chrome registered; runtime validation pending")


if __name__ == "__main__":
    main()
