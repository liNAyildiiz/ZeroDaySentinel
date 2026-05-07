from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SUMMARY_FILE = ROOT_DIR / "reports" / "summary.json"
ALERTS_FILE = ROOT_DIR / "reports" / "alerts.json"
EVENTS_FILE = ROOT_DIR / "lab" / "sample-logs" / "sample_events.jsonl"
ANALYTICS_FILE = ROOT_DIR / "reports" / "triage_analytics.json"
OUTPUT_FILE = ROOT_DIR / "dashboard" / "index.html"


def load_json(path: Path, fallback):
    if not path.exists():
        return fallback
    return json.loads(path.read_text(encoding="utf-8-sig"))


def load_events(path: Path) -> list[dict]:
    events: list[dict] = []

    if not path.exists():
        return events

    for line in path.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if line:
            events.append(json.loads(line))

    return events


def counter_to_rows(counter: Counter) -> str:
    if not counter:
        return "<tr><td>No data</td><td>0</td></tr>"

    rows = []
    for key, value in counter.most_common():
        rows.append(f"<tr><td>{key}</td><td>{value}</td></tr>")
    return "\n".join(rows)


def dict_to_rows(data: dict) -> str:
    if not data:
        return "<tr><td>No data</td><td>0</td></tr>"

    rows = []
    for key, value in data.items():
        rows.append(f"<tr><td>{key}</td><td>{value}</td></tr>")
    return "\n".join(rows)


def render_dashboard(summary: dict, alerts: list[dict], events: list[dict], analytics: dict) -> str:
    priority_counts = Counter(alert.get("priority", "unknown") for alert in alerts)
    event_type_counts = Counter(event.get("event_type", "unknown") for event in events)

    total_events = summary.get("total_events", 0)
    total_alerts = summary.get("total_alerts", 0)
    alert_rate = summary.get("alert_rate", 0)

    triage_pressure_score = analytics.get("triage_pressure_score", "not generated")

    priority_rows = counter_to_rows(priority_counts)
    event_type_rows = counter_to_rows(event_type_counts)
    top_hosts_rows = dict_to_rows(analytics.get("top_hosts", {}))
    top_users_rows = dict_to_rows(analytics.get("top_users", {}))
    rule_hit_rows = dict_to_rows(analytics.get("rule_hit_counts", {}))
    recommended_action_rows = dict_to_rows(analytics.get("recommended_action_counts", {}))

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>ZeroDaySentinel Dashboard</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body {{
      margin: 0;
      font-family: Arial, sans-serif;
      background: #0f172a;
      color: #e5e7eb;
    }}
    header {{
      padding: 32px;
      background: #111827;
      border-bottom: 1px solid #334155;
    }}
    main {{
      padding: 32px;
      max-width: 1200px;
      margin: auto;
    }}
    h1, h2 {{
      margin-top: 0;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 16px;
      margin-bottom: 28px;
    }}
    .card {{
      background: #111827;
      border: 1px solid #334155;
      border-radius: 16px;
      padding: 20px;
    }}
    .metric {{
      font-size: 34px;
      font-weight: 700;
      margin-top: 8px;
    }}
    .metric-small {{
      font-size: 26px;
      font-weight: 700;
      margin-top: 8px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 12px;
    }}
    th, td {{
      border-bottom: 1px solid #334155;
      padding: 12px;
      text-align: left;
      vertical-align: top;
    }}
    th {{
      color: #93c5fd;
    }}
    .safe {{
      color: #86efac;
      font-weight: 700;
    }}
    .warning {{
      color: #facc15;
      font-weight: 700;
    }}
    .note {{
      color: #cbd5e1;
      line-height: 1.6;
    }}
  </style>
</head>
<body>
  <header>
    <h1>ZeroDaySentinel Dashboard</h1>
    <p class="note">Safe local dashboard generated from synthetic defensive telemetry and triage analytics.</p>
  </header>

  <main>
    <section class="grid">
      <div class="card">
        <h2>Total Events</h2>
        <div class="metric">{total_events}</div>
      </div>
      <div class="card">
        <h2>Total Alerts</h2>
        <div class="metric">{total_alerts}</div>
      </div>
      <div class="card">
        <h2>Alert Rate</h2>
        <div class="metric">{alert_rate}</div>
      </div>
      <div class="card">
        <h2>Triage Pressure Score</h2>
        <div class="metric-small warning">{triage_pressure_score}</div>
      </div>
      <div class="card">
        <h2>Safety</h2>
        <div class="metric safe">Defensive</div>
      </div>
    </section>

    <section class="grid">
      <div class="card">
        <h2>Alert Priority Distribution</h2>
        <table>
          <thead><tr><th>Priority</th><th>Count</th></tr></thead>
          <tbody>{priority_rows}</tbody>
        </table>
      </div>

      <div class="card">
        <h2>Event Type Distribution</h2>
        <table>
          <thead><tr><th>Event Type</th><th>Count</th></tr></thead>
          <tbody>{event_type_rows}</tbody>
        </table>
      </div>
    </section>

    <section class="grid">
      <div class="card">
        <h2>Top Hosts</h2>
        <table>
          <thead><tr><th>Host</th><th>Alerts</th></tr></thead>
          <tbody>{top_hosts_rows}</tbody>
        </table>
      </div>

      <div class="card">
        <h2>Top Users</h2>
        <table>
          <thead><tr><th>User</th><th>Alerts</th></tr></thead>
          <tbody>{top_users_rows}</tbody>
        </table>
      </div>
    </section>

    <section class="grid">
      <div class="card">
        <h2>Rule Hit Counts</h2>
        <table>
          <thead><tr><th>Rule</th><th>Hits</th></tr></thead>
          <tbody>{rule_hit_rows}</tbody>
        </table>
      </div>

      <div class="card">
        <h2>Recommended Actions</h2>
        <table>
          <thead><tr><th>Action</th><th>Count</th></tr></thead>
          <tbody>{recommended_action_rows}</tbody>
        </table>
      </div>
    </section>

    <section class="card">
      <h2>Safety Boundary</h2>
      <p class="note">
        This dashboard is generated only from synthetic local telemetry and defensive analytics.
        It does not include exploit code, payloads, bypass techniques, persistence logic,
        evasion logic, unauthorized testing instructions, or internet-wide scanning tools.
      </p>
    </section>
  </main>
</body>
</html>
"""


def main() -> None:
    summary = load_json(SUMMARY_FILE, {})
    alerts = load_json(ALERTS_FILE, [])
    analytics = load_json(ANALYTICS_FILE, {})
    events = load_events(EVENTS_FILE)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(render_dashboard(summary, alerts, events, analytics), encoding="utf-8")

    print(f"[ZeroDaySentinel] Dashboard generated: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
