"""Offline contract tests; no Gecko integration is implied."""
import importlib.util
from pathlib import Path
import unittest

SOURCE = Path(__file__).resolve().parents[1] / "modules/network-policy/policy.py"
spec = importlib.util.spec_from_file_location("nolp_network_policy", SOURCE)
module = importlib.util.module_from_spec(spec)
import sys
sys.modules[spec.name] = module
spec.loader.exec_module(module)


class PolicyTests(unittest.TestCase):
    def test_exact_match_and_normalization(self):
        policy = module.Policy.create(blocked_hosts=["EXAMPLE.COM."])
        self.assertEqual(policy.evaluate("example.com").action, module.Action.BLOCK)
        self.assertEqual(policy.evaluate("sub.example.com").action, module.Action.ALLOW)

    def test_exception_wins(self):
        policy = module.Policy.create(["example.com"], ["example.com"])
        self.assertEqual(policy.evaluate("EXAMPLE.com").reason, "explicit-exception")

    def test_unicode_domain(self):
        policy = module.Policy.create(["bücher.example"])
        self.assertEqual(policy.evaluate("xn--bcher-kva.example").action, module.Action.BLOCK)

    def test_invalid_input_rejected(self):
        for host in ["", "https://example.com", "example.com/path", "user@example.com", "-bad.example", "a..b", "127.0.0.1"]:
            with self.subTest(host=host), self.assertRaises(ValueError):
                module.normalize_host(host)

    def test_default_allow(self):
        self.assertEqual(module.Policy.create().evaluate("mozilla.org").action, module.Action.ALLOW)


if __name__ == "__main__":
    unittest.main()
