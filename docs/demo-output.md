# Demo Output

This document explains the current ZeroDaySentinel v0.2 local demo.

## Run the Demo

From the repository root:

python lab/log-generator/generate_logs.py
python lab/detector/detector.py

## Expected Output

A successful run produces output similar to:

[ZeroDaySentinel] Generated 120 synthetic events.
[ZeroDaySentinel] Detection completed.
[ZeroDaySentinel] Events analyzed: 120
[ZeroDaySentinel] Alerts generated: 25

## Generated Files

### lab/sample-logs/sample_events.jsonl

Contains synthetic JSONL telemetry events. Each line represents one event.

### reports/alerts.json

Contains generated defensive alerts. Each alert includes event ID, timestamp, host, user, source, event type, risk score, priority, matched rules, and recommended action.

### reports/summary.json

Contains a summary of the detection run, including total events, total alerts, alert rate, priority distribution, and safety metadata.

## Safety Statement

The demo uses only synthetic telemetry and non-weaponized defensive detection logic. It does not include exploit code, payloads, bypasses, persistence, evasion, or instructions for unauthorized access.
