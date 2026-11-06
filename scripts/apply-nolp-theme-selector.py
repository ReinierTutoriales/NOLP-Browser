#!/usr/bin/env python3
"""Install the NOLP theme picker in Firefox's privileged about:preferences."""
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "integrations/firefox-chrome"
PREFS = Path("browser/components/preferences/preferences.xhtml")
JAR = Path("browser/components/preferences/jar.mn")
SCRIPT_ANCHOR = '<script src="chrome://browser/content/preferences/preferences.js"/>'
SCRIPT = '<script type="module" src="chrome://browser/content/preferences/nolp/nolp-theme-preferences.mjs"></script>'
BODY_ANCHOR = '<vbox id="mainPrefPane">'
CONTROL = '''<html:div id="nolp-theme-preferences" role="group" aria-label="NOLP appearance">
          <html:label for="nolp-theme-select">NOLP theme</html:label>
          <html:select id="nolp-theme-select" aria-label="NOLP theme">
            <html:option value="light">NOLP Light</html:option>
            <html:option value="dark">NOLP Dark</html:option>
          </html:select>
        </html:div>'''
JAR_ANCHOR = "   content/browser/preferences/preferences.js"
RESOURCES = ("NolpThemeSelector.sys.mjs", "nolp-theme-preferences.mjs")


def apply(root: Path, check: bool = False) -> None:
    prefs, jar = root / PREFS, root / JAR
    if not (root / "mach").is_file() or not prefs.is_file() or not jar.is_file():
        raise ValueError("Unsupported Firefox source tree")
    page, manifest = prefs.read_text(), jar.read_text()
    if SCRIPT_ANCHOR not in page or BODY_ANCHOR not in page or JAR_ANCHOR not in manifest:
        raise ValueError("Firefox preferences layout changed")
    entries = [f"   content/browser/preferences/nolp/{name}" for name in RESOURCES]
    dest = prefs.parent / "nolp"
    for name in RESOURCES:
        if (dest / name).exists() and (dest / name).read_bytes() != (SOURCE / name).read_bytes():
            raise ValueError("Existing NOLP resource differs")
    if check:
        if SCRIPT not in page or CONTROL not in page or any(e not in manifest for e in entries):
            raise ValueError("NOLP theme picker not installed")
        if any(not (dest / name).is_file() for name in RESOURCES):
            raise ValueError("NOLP theme picker resource missing")
        return
    if SCRIPT not in page:
        page = page.replace(SCRIPT_ANCHOR, SCRIPT_ANCHOR + "\n  " + SCRIPT, 1)
    if CONTROL not in page:
        page = page.replace(BODY_ANCHOR, BODY_ANCHOR + "\n        " + CONTROL, 1)
    for entry in entries:
        if entry not in manifest:
            manifest = manifest.replace(JAR_ANCHOR, JAR_ANCHOR + "\n" + entry, 1)
    prefs.write_text(page)
    jar.write_text(manifest)
    dest.mkdir(exist_ok=True)
    for name in RESOURCES:
        (dest / name).write_bytes((SOURCE / name).read_bytes())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--firefox-dir", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        apply(args.firefox_dir, args.check)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
