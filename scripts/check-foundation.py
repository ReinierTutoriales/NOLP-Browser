#!/usr/bin/env python3
"""Validate NOLP Firefox upstream manifest without fetching or building."""
import pathlib
import re
import tomllib

root = pathlib.Path(__file__).resolve().parents[1]
data = tomllib.loads((root / "engine/upstream-manifest/firefox.toml").read_text())
assert data["firefox"]["source"] == "https://github.com/mozilla-firefox/firefox"
assert re.fullmatch(r"[0-9a-f]{40}", data["firefox"]["revision"])
assert (root / "scripts/bootstrap-firefox.sh").is_file()
print("NOLP foundation manifest valid:", data["firefox"]["revision"])
