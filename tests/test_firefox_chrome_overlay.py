"""Offline regression tests for Firefox chrome overlay registration."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/apply-firefox-chrome.py"
spec = importlib.util.spec_from_file_location("nolp_chrome", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class FirefoxChromeOverlayTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "mach").write_text("#!/bin/sh\n", encoding="utf-8")
        css = self.root / module.TARGET
        jar = self.root / module.JAR_PATH
        css.parent.mkdir(parents=True)
        css.write_text('/* browser theme */\n' + module.ANCHOR + '\n', encoding="utf-8")
        jar.write_text('  ' + module.JAR_ANCHOR + ' (../shared/browser-shared.css)\n', encoding="utf-8")

    def test_install_and_verify(self):
        module.apply(self.root)
        module.apply(self.root, check=True)
        css = (self.root / module.TARGET).read_text()
        jar = (self.root / module.JAR_PATH).read_text()
        self.assertEqual(css.count(module.IMPORT), 1)
        self.assertEqual(jar.count(module.JAR_ENTRY), 1)

    def test_idempotent(self):
        module.apply(self.root)
        before = ((self.root / module.TARGET).read_bytes(),
                  (self.root / module.JAR_PATH).read_bytes())
        module.apply(self.root)
        after = ((self.root / module.TARGET).read_bytes(),
                 (self.root / module.JAR_PATH).read_bytes())
        self.assertEqual(before, after)

    def test_check_fails_before_install(self):
        with self.assertRaisesRegex(ValueError, "missing"):
            module.apply(self.root, check=True)

    def test_upstream_layout_change_fails_closed(self):
        (self.root / module.TARGET).write_text("/* unexpected */", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "changed"):
            module.apply(self.root)

    def test_existing_modified_overlay_is_preserved(self):
        module.apply(self.root)
        overlay = (self.root / module.TARGET).parent / "nolp-chrome.css"
        overlay.write_text("changed", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "differs"):
            module.apply(self.root)
        self.assertEqual(overlay.read_text(), "changed")


if __name__ == "__main__":
    unittest.main()
