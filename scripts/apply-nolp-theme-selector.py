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


# Native about:preferences integration: packaged resources and one accessible control.
PREFS = Path("browser/components/preferences/preferences.xhtml")
PREFS_JAR = Path("browser/components/preferences/jar.mn")
SELECTOR = Path(__file__).resolve().parents[1] / "integrations/firefox-chrome/NolpThemeSelector.sys.mjs"
PREFS_UI = Path(__file__).resolve().parents[1] / "integrations/firefox-chrome/nolp-theme-preferences.mjs"
PREFS_ANCHOR = '<script src="chrome://browser/content/preferences/preferences.js"/>'
PREFS_SCRIPT = '<script type="module" src="chrome://browser/content/preferences/nolp/nolp-theme-preferences.mjs"></script>'
PREFS_BODY_ANCHOR = '<vbox id="mainPrefPane">'
PREFS_CONTROL = '''<html:div id="nolp-theme-preferences" role="group" aria-label="NOLP appearance">
          <html:label for="nolp-theme-select">NOLP theme</html:label>
          <html:select id="nolp-theme-select" aria-label="NOLP theme">
            <html:option value="light">NOLP Light</html:option>
            <html:option value="dark">NOLP Dark</html:option>
          </html:select>
        </html:div>'''
PREFS_JAR_ANCHOR = "   content/browser/preferences/preferences.js"
PREFS_JAR_LINES = (
    "   content/browser/preferences/nolp/NolpThemeSelector.sys.mjs      (../../integrations/firefox-chrome/NolpThemeSelector.sys.mjs)",
    "   content/browser/preferences/nolp/nolp-theme-preferences.mjs      (../../integrations/firefox-chrome/nolp-theme-preferences.mjs)",
)

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
        lines = manifest.splitlines(keepends=True)
        anchor_indices = [i for i, line in enumerate(lines) if JAR_ANCHOR in line]
        if len(anchor_indices) != 1:
            raise ValueError("Ambiguous Firefox chrome packaging anchor")
        lines.insert(anchor_indices[0] + 1, JAR_ENTRY + "\n")
        manifest = "".join(lines)
    prefs = root / PREFS
    prefs_jar = root / PREFS_JAR
    if not prefs.is_file() or not prefs_jar.is_file():
        raise ValueError("Firefox preferences source unavailable")
    prefs_text = prefs.read_text(encoding="utf-8")
    prefs_manifest = prefs_jar.read_text(encoding="utf-8")
    if PREFS_ANCHOR not in prefs_text or PREFS_BODY_ANCHOR not in prefs_text or PREFS_JAR_ANCHOR not in prefs_manifest:
        raise ValueError("Firefox preferences integration points changed")
    if any(prefs_text.count(x) > 1 for x in (PREFS_SCRIPT, PREFS_CONTROL)):
        raise ValueError("Duplicate NOLP preference controls")
    if any(prefs_manifest.count(x) > 1 for x in PREFS_JAR_LINES):
        raise ValueError("Duplicate NOLP preference resources")
    prefs_dir = prefs.parent / "nolp"
    resources = ((prefs_dir / "NolpThemeSelector.sys.mjs", SELECTOR),
                 (prefs_dir / "nolp-theme-preferences.mjs", PREFS_UI))
    for dest_resource, source_resource in resources:
        if dest_resource.exists() and dest_resource.read_bytes() != source_resource.read_bytes():
            raise ValueError("Existing NOLP preference resource differs")
    if check:
        if PREFS_SCRIPT not in prefs_text or PREFS_CONTROL not in prefs_text or any(line not in prefs_manifest for line in PREFS_JAR_LINES):
            raise ValueError("NOLP preferences integration missing")
        if any(not dest_resource.is_file() for dest_resource, _ in resources):
            raise ValueError("NOLP preferences resources missing")
    else:
        if PREFS_SCRIPT not in prefs_text:
            prefs_text = prefs_text.replace(PREFS_ANCHOR, PREFS_ANCHOR + "\\n  " + PREFS_SCRIPT, 1)
        if PREFS_CONTROL not in prefs_text:
            prefs_text = prefs_text.replace(PREFS_BODY_ANCHOR, PREFS_BODY_ANCHOR + "\\n        " + PREFS_CONTROL, 1)
        if any(line not in prefs_manifest for line in PREFS_JAR_LINES):
            prefs_manifest = prefs_manifest.replace(PREFS_JAR_ANCHOR, PREFS_JAR_ANCHOR + "\\n" + "\\n".join(line for line in PREFS_JAR_LINES if line not in prefs_manifest), 1)
        prefs.write_text(prefs_text, encoding="utf-8")
        prefs_jar.write_text(prefs_manifest, encoding="utf-8")
        prefs_dir.mkdir(exist_ok=True)
        for dest_resource, source_resource in resources:
            dest_resource.write_bytes(source_resource.read_bytes())
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
