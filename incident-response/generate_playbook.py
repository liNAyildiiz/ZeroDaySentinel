from __future__ import annotations

import json
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
ANALYTICS_FILE = ROOT_DIR / "reports" / "triage_analytics.json"
OUTPUT_FILE = ROOT_DIR / "incident-response" / "generated_playbook.md"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def render_table(title: str, data: dict, key_name: str, value_name: str) -> str:
    lines = [
        f"## {title}",
        "",
        f"| {key_name} | {value_name} |",
        "|---|---|",
    ]

    if not data:
        lines.append("| No data | 0 |")
    else:
        for key, value in data.items():
            lines.append(f"| {key} | {value} |")

    return "\n".join(lines)


def severity_guidance(priority_counts: dict) -> str:
    critical = int(priority_counts.get("critical", 0))
    high = int(priority_counts.get("high", 0))
    medium = int(priority_counts.get("medium", 0))

    lines = [
        "## Severity-Based Response Guidance",
        "",
        "| Severity | Count | Defensive Response |",
        "|---|---:|---|",
        f"| Critical | {critical} | Immediately review related synthetic alerts, identify affected host/user context, preserve local evidence, and escalate for defensive containment review. |",
        f"| High | {high} | Prioritize alert validation, correlate with rule hits, and prepare a focused investigation checklist. |",
        f"| Medium | {medium} | Review after critical and high items; use for trend observation and rule tuning. |",
    ]

    return "\n".join(lines)


def render_playbook(analytics: dict) -> str:
    priority_counts = analytics.get("priority_counts", {})
    top_hosts = analytics.get("top_hosts", {})
    top_users = analytics.get("top_users", {})
    rule_hit_counts = analytics.get("rule_hit_counts", {})
    recommended_actions = analytics.get("recommended_action_counts", {})
    triage_score = analytics.get("triage_pressure_score", 0)

    sections = [
        "# ZeroDaySentinel Incident Response Playbook",
        "",
        "This playbook is generated from synthetic defensive telemetry and triage analytics. It is intended for local blue-team review and structured response planning.",
        "",
        "## Executive Triage Summary",
        "",
        f"- Triage pressure score: `{triage_score}`",
        f"- Total alerts: `{analytics.get('total_alerts', 0)}`",
        f"- Total synthetic events: `{analytics.get('total_events', 0)}`",
        f"- Alert rate: `{analytics.get('alert_rate', 0)}`",
        "",
        "The triage pressure score helps estimate how much defensive review effort the latest local synthetic run may require.",
        "",
        severity_guidance(priority_counts),
        "",
        render_table(
            "Top Host Triage Queue",
            top_hosts,
            "Host",
            "Alert Count",
        ),
        "",
        render_table(
            "Top User Triage Queue",
            top_users,
            "User",
            "Alert Count",
        ),
        "",
        render_table(
            "Rule-Based Response Mapping",
            rule_hit_counts,
            "Rule",
            "Hits",
        ),
        "",
        render_table(
            "Recommended Defensive Actions",
            recommended_actions,
            "Recommended Action",
            "Count",
        ),
        "",
        "## Suggested Defensive Workflow",
        "",
        "1. Review critical alerts first.",
        "2. Correlate top hosts and top users with rule hit counts.",
        "3. Validate whether repeated alerts are caused by the same synthetic behavior pattern.",
        "4. Document findings in the defensive detection report.",
        "5. Use the recommended actions table to prioritize containment review, monitoring, or rule tuning.",
        "",
        "## Safety Boundary",
        "",
        "This playbook is defensive, synthetic, and non-weaponized. It does not include exploit code, payloads, bypass techniques, persistence logic, evasion logic, unauthorized testing instructions, or internet-wide scanning tools.",
        "",
    ]

    return "\n".join(sections)


def main() -> None:
    analytics = load_json(ANALYTICS_FILE)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(render_playbook(analytics), encoding="utf-8")

    print(f"[ZeroDaySentinel] Incident response playbook generated: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
