from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SUMMARY_FILE = ROOT_DIR / "reports" / "summary.json"
ALERTS_FILE = ROOT_DIR / "reports" / "alerts.json"
SAMPLE_EVENTS_FILE = ROOT_DIR / "lab" / "sample-logs" / "sample_events.jsonl"


class ZeroDaySentinelDemoTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.run(
            [sys.executable, "sentinel.py", "--demo"],
            cwd=ROOT_DIR,
            check=True,
        )

    def test_demo_outputs_exist(self) -> None:
        self.assertTrue(SAMPLE_EVENTS_FILE.exists())
        self.assertTrue(ALERTS_FILE.exists())
        self.assertTrue(SUMMARY_FILE.exists())

    def test_summary_contract(self) -> None:
        summary = json.loads(SUMMARY_FILE.read_text(encoding="utf-8"))

        self.assertEqual(summary["project"], "ZeroDaySentinel")
        self.assertEqual(summary["dataset"], "synthetic-telemetry-v0.2")
        self.assertEqual(summary["total_events"], 120)
        self.assertEqual(summary["total_alerts"], 25)
        self.assertFalse(summary["contains_exploit_code"])
        self.assertTrue(summary["safe_for_local_demo"])

    def test_alerts_are_defensive_and_structured(self) -> None:
        alerts = json.loads(ALERTS_FILE.read_text(encoding="utf-8"))

        self.assertEqual(len(alerts), 25)

        for alert in alerts:
            self.assertIn("alert_id", alert)
            self.assertIn("event_id", alert)
            self.assertIn("risk_score", alert)
            self.assertIn("priority", alert)
            self.assertIn("matched_rules", alert)
            self.assertGreaterEqual(alert["risk_score"], 60)
            self.assertGreaterEqual(len(alert["matched_rules"]), 1)
            self.assertEqual(alert["recommended_action"], "triage_required")


if __name__ == "__main__":
    unittest.main()
