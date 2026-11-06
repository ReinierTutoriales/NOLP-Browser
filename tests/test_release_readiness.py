"""Release gate regression tests: fail closed, including stale successful runs."""
import importlib.util
from pathlib import Path
import unittest

SOURCE = Path(__file__).resolve().parents[1] / "scripts/check-release-readiness.py"
spec = importlib.util.spec_from_file_location("release_readiness", SOURCE)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


def run(name, status="completed", conclusion="success", run_id=1):
    return {"name": name, "status": status, "conclusion": conclusion, "id": run_id}


class ReleaseReadinessTests(unittest.TestCase):
    def test_all_six_successful(self):
        checks = {name: [run(name)] for name in gate.REQUIRED}
        self.assertEqual(gate.evaluate_runs(checks), [])

    def test_missing_check_blocks(self):
        checks = {name: [run(name)] for name in gate.REQUIRED}
        missing = sorted(gate.REQUIRED)[0]
        del checks[missing]
        self.assertEqual(gate.evaluate_runs(checks), [missing])

    def test_failed_check_blocks(self):
        checks = {name: [run(name)] for name in gate.REQUIRED}
        failed = sorted(gate.REQUIRED)[0]
        checks[failed] = [run(failed, conclusion="failure")]
        self.assertEqual(gate.evaluate_runs(checks), [failed])

    def test_pending_check_blocks(self):
        checks = {name: [run(name)] for name in gate.REQUIRED}
        pending = sorted(gate.REQUIRED)[0]
        checks[pending] = [run(pending, status="in_progress", conclusion=None)]
        self.assertEqual(gate.evaluate_runs(checks), [pending])

    def test_newer_failure_overrides_older_success(self):
        checks = {name: [run(name)] for name in gate.REQUIRED}
        name = sorted(gate.REQUIRED)[0]
        checks[name] = [run(name, run_id=1), run(name, conclusion="failure", run_id=2)]
        self.assertEqual(gate.evaluate_runs(checks), [name])


if __name__ == "__main__":
    unittest.main()
