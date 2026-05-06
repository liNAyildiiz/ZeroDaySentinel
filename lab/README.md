# Synthetic Telemetry Lab

This lab contains the first working ZeroDaySentinel demo.

It does not include exploit code, payloads, bypasses, persistence, evasion, or instructions for unauthorized access.

## Components

- `log-generator/generate_logs.py` creates synthetic security telemetry.
- `detector/detector.py` analyzes synthetic events and generates defensive alerts.
- `sample-logs/sample_events.jsonl` stores generated local demo events.
- `reports/alerts.json` contains generated alerts.
- `reports/summary.json` contains a summary of detection results.

## Run Locally

From the repository root:

```powershell
python lab/log-generator/generate_logs.py
python lab/detector/detector.py
```

If `python` is not available on Windows, try:

```powershell
py lab/log-generator/generate_logs.py
py lab/detector/detector.py
```

## Safety

All events are synthetic and non-weaponized. The detector performs defensive scoring only.
