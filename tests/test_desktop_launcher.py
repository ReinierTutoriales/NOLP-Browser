"""Static regression checks for the Linux development launcher."""
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
LAUNCHER = ROOT / "scripts/run-nolp-desktop.sh"


class DesktopLauncherTests(unittest.TestCase):
    def test_bash_syntax(self):
        subprocess.run(["bash", "-n", str(LAUNCHER)], check=True)

    def test_invalid_url_rejected_without_firefox(self):
        for value in ("http://example.org", "file:///etc/passwd", "javascript:alert(1)"):
            with self.subTest(value=value):
                result = subprocess.run(["bash", str(LAUNCHER), value],
                                        capture_output=True, text=True, timeout=10)
                self.assertEqual(result.returncode, 2)
                self.assertIn("Only HTTPS", result.stderr)

    def test_extra_arguments_rejected(self):
        result = subprocess.run(["bash", str(LAUNCHER), "about:blank", "unexpected"],
                                capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
