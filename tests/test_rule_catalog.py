from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
CATALOG_FILE = ROOT_DIR / "detection" / "rules" / "catalog.json"


class DetectionRuleCatalogTest(unittest.TestCase):
    def test_catalog_exists_and_is_valid(self) -> None:
        self.assertTrue(CATALOG_FILE.exists())

        catalog = json.loads(CATALOG_FILE.read_text(encoding="utf-8-sig"))

        self.assertEqual(catalog["project"], "ZeroDaySentinel")
        self.assertEqual(catalog["catalog_type"], "defensive_detection_rules")
        self.assertTrue(catalog["safety_boundary"]["defensive_only"])
        self.assertFalse(catalog["safety_boundary"]["contains_exploit_code"])
        self.assertEqual(len(catalog["rules"]), 6)

    def test_each_rule_has_required_fields(self) -> None:
        catalog = json.loads(CATALOG_FILE.read_text(encoding="utf-8-sig"))

        required_fields = {
            "rule_id",
            "name",
            "severity",
            "data_source",
            "defensive_objective",
            "triage_hint",
            "response_mapping",
            "safety_boundary",
        }

        for rule in catalog["rules"]:
            self.assertTrue(required_fields.issubset(rule.keys()))
            self.assertTrue(rule["rule_id"].startswith("ZDS-"))
            self.assertIn(rule["severity"], {"low", "medium", "high", "critical"})
            self.assertNotIn("payload", rule["safety_boundary"].lower())


if __name__ == "__main__":
    unittest.main()
