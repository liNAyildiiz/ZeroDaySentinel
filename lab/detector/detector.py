from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[2]
INPUT_FILE = ROOT_DIR / "lab" / "sample-logs" / "sample_events.jsonl"
ALERTS_FILE = ROOT_DIR / "reports" / "alerts.json"
SUMMARY_FILE = ROOT_DIR / "reports" / "summary.json"


@dataclass(frozen=True)
class DetectionRule:
    rule_id: str
    name: str
    description: str
    event_types: set[str]
    labels: set[str]
    weight: int


RULES = [
    DetectionRule(
        rule_id="ZDS-001",
        name="Authentication Anomaly Burst",
        description="Detects synthetic bursts of failed authentication behavior.",
        event_types={"auth_failure_burst"},
        labels={"repeated_failure", "identity_anomaly"},
        weight=30,
    ),
    DetectionRule(
        rule_id="ZDS-002",
        name="Unexpected Execution Context",
        description="Detects synthetic process-tree behavior that deviates from normal baselines.",
        event_types={"unexpected_child_process"},
        labels={"process_tree_anomaly", "unexpected_execution_context"},
        weight=35,
    ),
    DetectionRule(
        rule_id="ZDS-003",
        name="Unusual Outbound Pattern",
        description="Detects synthetic rare outbound communication behavior.",
        event_types={"unusual_outbound_pattern"},
        labels={"rare_destination", "network_frequency_anomaly"},
        weight=30,
    ),
    DetectionRule(
        rule_id="ZDS-004",
        name="Sensitive Access Pattern",
        description="Detects synthetic access behavior involving sensitive areas.",
        event_types={"sensitive_file_access_pattern"},
        labels={"sensitive_path_touch", "access_pattern_anomaly"},
        weight=25,
    ),
    DetectionRule(
        rule_id="ZDS-005",
        name="Rare Privileged Operation",
        description="Detects synthetic rare administrative activity.",
        event_types={"rare_admin_action"},
        labels={"privileged_action", "rare_operation"},
        weight=25,
    ),
    DetectionRule(
        rule_id="ZDS-006",
        name="Abnormal API Frequency",
        description="Detects synthetic high-frequency API behavior.",
        event_types={"abnormal_api_frequency"},
        labels={"request_rate_anomaly", "behavioral_outlier"},
        weight=25,
    ),
]


def load_events(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(
            f"Input file not found: {path}. Run lab/log-generator/generate_logs.py first."
        )

    events: list[dict[str, Any]] = []

    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            if not line:
                continue

            try:
                events.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on line {line_number}: {exc}") from exc

    return events


def evaluate_event(event: dict[str, Any]) -> dict[str, Any] | None:
    event_type = str(event.get("event_type", ""))
    labels = set(event.get("labels", []))
    base_score = int(event.get("risk_hint", 0))

    matched_rules: list[dict[str, str]] = []
    score = base_score

    for rule in RULES:
        event_type_match = event_type in rule.event_types
        label_match = bool(labels.intersection(rule.labels))

        if event_type_match or label_match:
            score += rule.weight
            matched_rules.append(
                {
                    "rule_id": rule.rule_id,
                    "name": rule.name,
                    "description": rule.description,
                }
            )

    score = min(score, 100)

    if score < 60:
        return None

    if score >= 90:
        priority = "critical"
    elif score >= 75:
        priority = "high"
    else:
        priority = "medium"

    return {
        "alert_id": f"alert-{event.get('event_id')}",
        "event_id": event.get("event_id"),
        "timestamp": event.get("timestamp"),
        "host": event.get("host"),
        "user": event.get("user"),
        "source": event.get("source"),
        "event_type": event_type,
        "risk_score": score,
        "priority": priority,
        "matched_rules": matched_rules,
        "recommended_action": "triage_required",
        "defensive_note": (
            "This alert is based on synthetic telemetry and non-weaponized detection logic."
        ),
    }


def build_summary(events: list[dict[str, Any]], alerts: list[dict[str, Any]]) -> dict[str, Any]:
    priority_counts = {"medium": 0, "high": 0, "critical": 0}

    for alert in alerts:
        priority = alert.get("priority", "medium")
        priority_counts[priority] = priority_counts.get(priority, 0) + 1

    return {
        "project": "ZeroDaySentinel",
        "dataset": "synthetic-telemetry-v0.2",
        "total_events": len(events),
        "total_alerts": len(alerts),
        "alert_rate": round(len(alerts) / len(events), 4) if events else 0,
        "priority_counts": priority_counts,
        "contains_exploit_code": False,
        "safe_for_local_demo": True,
        "next_step": "Review reports/alerts.json and map detections to defensive response playbooks.",
    }


def main() -> None:
    events = load_events(INPUT_FILE)
    alerts = [alert for event in events if (alert := evaluate_event(event)) is not None]
    summary = build_summary(events, alerts)

    ALERTS_FILE.parent.mkdir(parents=True, exist_ok=True)

    with ALERTS_FILE.open("w", encoding="utf-8") as file:
        json.dump(alerts, file, indent=2, ensure_ascii=False)

    with SUMMARY_FILE.open("w", encoding="utf-8") as file:
        json.dump(summary, file, indent=2, ensure_ascii=False)

    print("[ZeroDaySentinel] Detection completed.")
    print(f"[ZeroDaySentinel] Events analyzed: {summary['total_events']}")
    print(f"[ZeroDaySentinel] Alerts generated: {summary['total_alerts']}")
    print(f"[ZeroDaySentinel] Alerts file: {ALERTS_FILE}")
    print(f"[ZeroDaySentinel] Summary file: {SUMMARY_FILE}")


if __name__ == "__main__":
    main()
