import importlib.util
from pathlib import Path
import tempfile
import unittest

script = Path(__file__).resolve().parents[1] / "scripts/apply-nolp-theme-selector.py"
spec = importlib.util.spec_from_file_location("selector", script)
selector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(selector)


class ThemeSelectorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "mach").write_text("mach")
        page = self.root / selector.PREFS
        jar = self.root / selector.JAR
        page.parent.mkdir(parents=True)
        page.write_text(selector.SCRIPT_ANCHOR + "\n" + selector.BODY_ANCHOR)
        jar.write_text(selector.JAR_ANCHOR + "\n")

    def test_install_check_idempotent(self):
        selector.apply(self.root)
        selector.apply(self.root, check=True)
        before = (self.root / selector.PREFS).read_bytes()
        selector.apply(self.root)
        self.assertEqual(before, (self.root / selector.PREFS).read_bytes())
        self.assertEqual((self.root / selector.JAR).read_text().count(selector.JAR_ANCHOR), 1)

    def test_auto_is_native_default_theme(self):
        controller = (selector.SOURCE / "NolpThemeSelector.sys.mjs").read_text()
        self.assertIn('auto: "default-theme@mozilla.org"', controller)
        self.assertNotIn("setInterval", controller)
        self.assertNotIn("matchMedia", controller)
        self.assertIn("Automático (sistema)", selector.CONTROL)

    def test_check_fails_before_install(self):
        with self.assertRaisesRegex(ValueError, "not installed"):
            selector.apply(self.root, check=True)

    def test_unexpected_upstream_layout_fails(self):
        (self.root / selector.PREFS).write_text("unexpected")
        with self.assertRaisesRegex(ValueError, "changed"):
            selector.apply(self.root)


if __name__ == "__main__":
    unittest.main()
