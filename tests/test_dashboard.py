from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
DASHBOARD_FILE = ROOT_DIR / "dashboard" / "index.html"


class DashboardGenerationTest(unittest.TestCase):
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
            [sys.executable, "dashboard/generate_dashboard.py"],
            cwd=ROOT_DIR,
            check=True,
        )

    def test_dashboard_file_exists(self) -> None:
        self.assertTrue(DASHBOARD_FILE.exists())

    def test_dashboard_contains_expected_sections(self) -> None:
        content = DASHBOARD_FILE.read_text(encoding="utf-8-sig")

        self.assertIn("ZeroDaySentinel Dashboard", content)
        self.assertIn("Total Events", content)
        self.assertIn("Total Alerts", content)
        self.assertIn("Alert Priority Distribution", content)
        self.assertIn("Event Type Distribution", content)
        self.assertIn("Safety Boundary", content)

    def test_dashboard_contains_analytics_sections(self) -> None:
        content = DASHBOARD_FILE.read_text(encoding="utf-8-sig")

        self.assertIn("Triage Pressure Score", content)
        self.assertIn("Top Hosts", content)
        self.assertIn("Top Users", content)
        self.assertIn("Rule Hit Counts", content)
        self.assertIn("Recommended Actions", content)


if __name__ == "__main__":
    unittest.main()
