#!/usr/bin/env python3
"""Regression checks for the NOLP native branding generator."""
import ast
from pathlib import Path
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/apply-nolp-branding.py"


class BrandingSourceTests(unittest.TestCase):
    def test_script_is_valid_python(self):
        ast.parse(SCRIPT.read_text(encoding="utf-8"), filename=str(SCRIPT))

    def test_native_branding_is_configured(self):
        source = SCRIPT.read_text(encoding="utf-8")
        self.assertIn('TARGET = Path("browser/branding/nolp")', source)
        self.assertIn('MOZ_APP_DISPLAYNAME=NOLP', source)
        self.assertIn('MOZ_MACBUNDLE_ID=org.nolp.browser', source)
        self.assertIn('icons = sorted(target.glob("default[0-9]*.png"))', source)
        self.assertIn('format="ICO"', source)
        self.assertIn('format="ICNS"', source)


if __name__ == "__main__":
    unittest.main()
