from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
ALERTS_FILE = ROOT_DIR / "reports" / "alerts.json"
SUMMARY_FILE = ROOT_DIR / "reports" / "summary.json"
OUTPUT_FILE = ROOT_DIR / "reports" / "triage_analytics.json"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def normalize(value: object, fallback: str = "unknown") -> str:
    if value is None:
        return fallback
    text = str(value).strip()
    return text if text else fallback


def count_rules(alerts: list[dict]) -> Counter:
    rule_counter: Counter = Counter()

    for alert in alerts:
        matched_rules = alert.get("matched_rules", [])

        if isinstance(matched_rules, list):
            for rule in matched_rules:
                rule_counter.update([normalize(rule)])
        else:
            rule_counter.update([normalize(matched_rules)])

    return rule_counter


def build_analytics(summary: dict, alerts: list[dict]) -> dict:
    priority_counts = Counter(normalize(alert.get("priority")) for alert in alerts)
    host_counts = Counter(normalize(alert.get("host")) for alert in alerts)
    user_counts = Counter(normalize(alert.get("user")) for alert in alerts)
    event_type_counts = Counter(normalize(alert.get("event_type")) for alert in alerts)
    action_counts = Counter(normalize(alert.get("recommended_action")) for alert in alerts)
    rule_counts = count_rules(alerts)

    total_alerts = len(alerts)
    critical_alerts = priority_counts.get("critical", 0)
    high_alerts = priority_counts.get("high", 0)

    triage_pressure_score = round(
        ((critical_alerts * 3) + (high_alerts * 2)) / max(total_alerts, 1),
        4,
    )

    return {
        "project": "ZeroDaySentinel",
        "dataset": summary.get("dataset", "synthetic-telemetry"),
        "total_events": summary.get("total_events", 0),
        "total_alerts": total_alerts,
        "alert_rate": summary.get("alert_rate", 0),
        "priority_counts": dict(priority_counts),
        "top_hosts": dict(host_counts.most_common(5)),
        "top_users": dict(user_counts.most_common(5)),
        "event_type_counts": dict(event_type_counts),
        "rule_hit_counts": dict(rule_counts.most_common()),
        "recommended_action_counts": dict(action_counts.most_common()),
        "triage_pressure_score": triage_pressure_score,
        "safety": {
            "synthetic_only": True,
            "contains_exploit_code": False,
            "contains_payloads": False,
            "contains_bypass_or_evasion_guidance": False,
            "contains_unauthorized_testing_instructions": False,
        },
        "next_step": "Use this analytics summary to prioritize defensive triage and response mapping.",
    }


def main() -> None:
    summary = load_json(SUMMARY_FILE)
    alerts = load_json(ALERTS_FILE)

    analytics = build_analytics(summary, alerts)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(analytics, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"[ZeroDaySentinel] Triage analytics generated: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
