from __future__ import annotations

import json
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
ANALYTICS_FILE = ROOT_DIR / "reports" / "triage_analytics.json"
SUMMARY_FILE = ROOT_DIR / "reports" / "summary.json"
OUTPUT_FILE = ROOT_DIR / "reports" / "detection_report.md"


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


def render_report(summary: dict, analytics: dict) -> str:
    total_events = analytics.get("total_events", summary.get("total_events", 0))
    total_alerts = analytics.get("total_alerts", summary.get("total_alerts", 0))
    alert_rate = analytics.get("alert_rate", summary.get("alert_rate", 0))
    triage_score = analytics.get("triage_pressure_score", 0)

    sections = [
        "# ZeroDaySentinel Defensive Detection Report",
        "",
        "This report summarizes the latest synthetic defensive telemetry run and triage analytics output.",
        "",
        "## Executive Summary",
        "",
        f"- Total synthetic events: `{total_events}`",
        f"- Total generated alerts: `{total_alerts}`",
        f"- Alert rate: `{alert_rate}`",
        f"- Triage pressure score: `{triage_score}`",
        "",
        "The triage pressure score is a defensive prioritization metric derived from generated synthetic alert priorities. It helps reviewers quickly understand whether the latest local run produced a low, moderate, or high triage load.",
        "",
        render_table(
            "Alert Priority Distribution",
            analytics.get("priority_counts", {}),
            "Priority",
            "Count",
        ),
        "",
        render_table(
            "Top Observed Hosts",
            analytics.get("top_hosts", {}),
            "Host",
            "Alerts",
        ),
        "",
        render_table(
            "Top Observed Users",
            analytics.get("top_users", {}),
            "User",
            "Alerts",
        ),
        "",
        render_table(
            "Rule Hit Summary",
            analytics.get("rule_hit_counts", {}),
            "Rule",
            "Hits",
        ),
        "",
        render_table(
            "Recommended Defensive Actions",
            analytics.get("recommended_action_counts", {}),
            "Action",
            "Count",
        ),
        "",
        "## Defensive Interpretation",
        "",
        "This report is designed for local blue-team review. It summarizes which synthetic hosts, users, event types, and rules should receive attention first during a defensive triage exercise.",
        "",
        "## Safety Boundary",
        "",
        "ZeroDaySentinel remains defensive, synthetic, and non-weaponized. This report is generated only from local synthetic telemetry and defensive alert metadata. It does not include exploit code, payloads, bypass techniques, persistence logic, evasion logic, unauthorized testing instructions, or internet-wide scanning tools.",
        "",
    ]

    return "\n".join(sections)


def main() -> None:
    summary = load_json(SUMMARY_FILE)
    analytics = load_json(ANALYTICS_FILE)

    OUTPUT_FILE.write_text(render_report(summary, analytics), encoding="utf-8")

    print(f"[ZeroDaySentinel] Detection report generated: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
