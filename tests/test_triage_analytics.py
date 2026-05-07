from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
ANALYTICS_FILE = ROOT_DIR / "reports" / "triage_analytics.json"


class TriageAnalyticsTest(unittest.TestCase):
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

    def load_analytics(self) -> dict:
        return json.loads(ANALYTICS_FILE.read_text(encoding="utf-8-sig"))

    def test_analytics_file_exists(self) -> None:
        self.assertTrue(ANALYTICS_FILE.exists())

    def test_analytics_contains_expected_fields(self) -> None:
        analytics = self.load_analytics()

        expected_fields = {
            "project",
            "dataset",
            "total_events",
            "total_alerts",
            "alert_rate",
            "priority_counts",
            "top_hosts",
            "top_users",
            "event_type_counts",
            "rule_hit_counts",
            "recommended_action_counts",
            "triage_pressure_score",
            "safety",
            "next_step",
        }

        self.assertTrue(expected_fields.issubset(analytics.keys()))

    def test_triage_pressure_score_is_numeric(self) -> None:
        analytics = self.load_analytics()
        self.assertIsInstance(analytics["triage_pressure_score"], float)
        self.assertGreaterEqual(analytics["triage_pressure_score"], 0)

    def test_safety_boundary(self) -> None:
        analytics = self.load_analytics()
        safety = analytics["safety"]

        self.assertTrue(safety["synthetic_only"])
        self.assertFalse(safety["contains_exploit_code"])
        self.assertFalse(safety["contains_payloads"])
        self.assertFalse(safety["contains_bypass_or_evasion_guidance"])
        self.assertFalse(safety["contains_unauthorized_testing_instructions"])


if __name__ == "__main__":
    unittest.main()
