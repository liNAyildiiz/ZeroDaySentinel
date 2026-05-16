from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
PLAYBOOK_FILE = ROOT_DIR / "incident-response" / "generated_playbook.md"


class IncidentResponsePlaybookTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.run(
            [sys.executable, "sentinel.py", "--demo"],
            cwd=ROOT_DIR,
            check=True,
        )
        subprocess.run(
            [sys.executable, "analytics/triage_analytics.py"],
            cwd=ROOT_DIR,
            check=True,
        )
        subprocess.run(
            [sys.executable, "incident-response/generate_playbook.py"],
            cwd=ROOT_DIR,
            check=True,
        )

    def test_playbook_file_exists(self) -> None:
        self.assertTrue(PLAYBOOK_FILE.exists())

    def test_playbook_contains_expected_sections(self) -> None:
        content = PLAYBOOK_FILE.read_text(encoding="utf-8-sig")

        self.assertIn("ZeroDaySentinel Incident Response Playbook", content)
        self.assertIn("Executive Triage Summary", content)
        self.assertIn("Severity-Based Response Guidance", content)
        self.assertIn("Top Host Triage Queue", content)
        self.assertIn("Top User Triage Queue", content)
        self.assertIn("Rule-Based Response Mapping", content)
        self.assertIn("Recommended Defensive Actions", content)
        self.assertIn("Suggested Defensive Workflow", content)
        self.assertIn("Safety Boundary", content)

    def test_playbook_preserves_safety_boundary(self) -> None:
        content = PLAYBOOK_FILE.read_text(encoding="utf-8-sig").lower()

        self.assertIn("defensive", content)
        self.assertIn("synthetic", content)
        self.assertIn("non-weaponized", content)
        self.assertIn("does not include exploit code", content)
        self.assertIn("unauthorized testing instructions", content)


if __name__ == "__main__":
    unittest.main()
