# ZeroDaySentinel Architecture

ZeroDaySentinel is a defensive zero-day readiness and detection engineering lab.

## Pipeline

Synthetic Telemetry Source
→ sample_events.jsonl
→ Defensive Detector
→ Rule Matching
→ Risk Scoring
→ alerts.json and summary.json

## Design Goals

The current prototype focuses on safe synthetic telemetry, defensive event analysis, simple rule-based scoring, explainable alert output, reproducible local execution, and non-weaponized detection logic.

## Current Components

### lab/log-generator/generate_logs.py

Generates synthetic local telemetry. The generated events include normal operational activity and suspicious behavior patterns. These events do not contain real exploit payloads or unauthorized activity instructions.

### lab/detector/detector.py

Reads synthetic telemetry, evaluates events against defensive rules, computes a risk score, and writes alert reports.

### detection/rules/sigma/

Contains Sigma-style detection examples for synthetic suspicious behavior.

### detection/rules/yara/

Contains YARA-style marker rules for non-weaponized synthetic behavior.

### reports/

Contains generated demo outputs, including alert details and summary statistics.

## Security Boundary

ZeroDaySentinel does not provide exploit code, weaponized proof-of-concept payloads, bypass techniques, stealth logic, persistence logic, unauthorized testing instructions, or internet-wide scanning tools.
