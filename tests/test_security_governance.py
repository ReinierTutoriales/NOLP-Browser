"""Security policy checks that run without external network access."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class SecurityGovernanceTests(unittest.TestCase):
    def test_mandatory_security_and_version_gates(self):
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        for name in ("security-assurance", "latest-stable-gate"):
            path = ROOT / "skills" / name / "SKILL.md"
            self.assertTrue(path.is_file(), f"Missing mandatory skill: {name}")
            self.assertIn(f"skills/{name}/SKILL.md", agents)

    def test_workflows_use_minimum_default_permissions(self):
        for workflow in (ROOT / ".github/workflows").glob("*.yml"):
            content = workflow.read_text(encoding="utf-8")
            self.assertRegex(content, r"(?m)^permissions:\s*\n\s+contents:\s*read\s*$",
                             f"{workflow.name} must declare read-only default permissions")

    def test_no_bypass_of_security_checks(self):
        for workflow in (ROOT / ".github/workflows").glob("*.yml"):
            content = workflow.read_text(encoding="utf-8")
            self.assertNotRegex(content, r"(?m)^\s*continue-on-error:\s*true\s*$",
                                f"{workflow.name} bypasses failed checks")


if __name__ == "__main__":
    unittest.main()
