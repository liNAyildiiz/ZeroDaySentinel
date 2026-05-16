from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
REPORT_FILE = ROOT_DIR / "reports" / "detection_report.md"


class DetectionReportTest(unittest.TestCase):
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
            [sys.executable, "reports/generate_detection_report.py"],
            cwd=ROOT_DIR,
            check=True,
        )

    def test_report_file_exists(self) -> None:
        self.assertTrue(REPORT_FILE.exists())

    def test_report_contains_expected_sections(self) -> None:
        content = REPORT_FILE.read_text(encoding="utf-8-sig")

        self.assertIn("ZeroDaySentinel Defensive Detection Report", content)
        self.assertIn("Executive Summary", content)
        self.assertIn("Alert Priority Distribution", content)
        self.assertIn("Top Observed Hosts", content)
        self.assertIn("Top Observed Users", content)
        self.assertIn("Rule Hit Summary", content)
        self.assertIn("Recommended Defensive Actions", content)
        self.assertIn("Defensive Interpretation", content)
        self.assertIn("Safety Boundary", content)

    def test_report_preserves_safety_boundary(self) -> None:
        content = REPORT_FILE.read_text(encoding="utf-8-sig")

        self.assertIn("defensive", content.lower())
        self.assertIn("synthetic", content.lower())
        self.assertIn("non-weaponized", content.lower())
        self.assertIn("does not include exploit code", content.lower())


if __name__ == "__main__":
    unittest.main()
