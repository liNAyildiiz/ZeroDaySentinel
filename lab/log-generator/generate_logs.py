from __future__ import annotations

import json
import random
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
OUTPUT_FILE = ROOT_DIR / "lab" / "sample-logs" / "sample_events.jsonl"

random.seed(42)


USERS = [
    "alice.research",
    "bob.admin",
    "carol.engineering",
    "david.ops",
    "service.backup",
]

HOSTS = [
    "win-endpoint-01",
    "linux-api-02",
    "k8s-node-03",
    "db-gateway-01",
    "build-runner-01",
]

SOURCES = [
    "web-api",
    "auth-service",
    "endpoint-agent",
    "kernel-telemetry-sim",
    "network-sensor-sim",
]


NORMAL_EVENT_TYPES = [
    "user_login_success",
    "scheduled_backup_completed",
    "service_health_check",
    "normal_api_request",
    "configuration_read",
    "package_update_check",
]


SUSPICIOUS_EVENT_TYPES = [
    "auth_failure_burst",
    "unexpected_child_process",
    "unusual_outbound_pattern",
    "sensitive_file_access_pattern",
    "rare_admin_action",
    "abnormal_api_frequency",
]


def iso_time(base_time: datetime, offset_minutes: int) -> str:
    return (base_time + timedelta(minutes=offset_minutes)).isoformat()


def build_event(event_type: str, suspicious: bool, index: int) -> dict:
    severity = "low"
    risk_hint = random.randint(1, 25)
    indicators: list[str] = []

    if suspicious:
        severity = random.choice(["medium", "high", "critical"])
        risk_hint = random.randint(55, 95)

        indicator_map = {
            "auth_failure_burst": ["repeated_failure", "identity_anomaly"],
            "unexpected_child_process": ["process_tree_anomaly", "unexpected_execution_context"],
            "unusual_outbound_pattern": ["rare_destination", "network_frequency_anomaly"],
            "sensitive_file_access_pattern": ["sensitive_path_touch", "access_pattern_anomaly"],
            "rare_admin_action": ["privileged_action", "rare_operation"],
            "abnormal_api_frequency": ["request_rate_anomaly", "behavioral_outlier"],
        }

        indicators = indicator_map.get(event_type, ["behavioral_anomaly"])

    return {
        "event_id": str(uuid.uuid4()),
        "timestamp": iso_time(
            datetime(2026, 5, 6, 18, 0, 0, tzinfo=timezone.utc),
            index,
        ),
        "source": random.choice(SOURCES),
        "host": random.choice(HOSTS),
        "user": random.choice(USERS),
        "event_type": event_type,
        "severity": severity,
        "risk_hint": risk_hint,
        "synthetic": True,
        "labels": indicators,
        "message": (
            "Synthetic suspicious behavior generated for defensive detection testing."
            if suspicious
            else "Synthetic normal operational event."
        ),
        "metadata": {
            "project": "ZeroDaySentinel",
            "dataset": "synthetic-telemetry-v0.2",
            "contains_exploit": False,
            "safe_for_local_demo": True,
        },
    }


def generate_events(total_events: int = 120, suspicious_ratio: float = 0.22) -> list[dict]:
    events: list[dict] = []

    for index in range(total_events):
        suspicious = random.random() < suspicious_ratio

        if suspicious:
            event_type = random.choice(SUSPICIOUS_EVENT_TYPES)
        else:
            event_type = random.choice(NORMAL_EVENT_TYPES)

        events.append(build_event(event_type, suspicious, index))

    return events


def main() -> None:
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    events = generate_events()

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        for event in events:
            file.write(json.dumps(event, ensure_ascii=False) + "\n")

    print(f"[ZeroDaySentinel] Generated {len(events)} synthetic events.")
    print(f"[ZeroDaySentinel] Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
