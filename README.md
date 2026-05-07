# ZeroDaySentinel 🛡️

ZeroDaySentinel is a defensive cybersecurity research project focused on zero-day readiness, detection engineering, threat modeling, synthetic telemetry, incident response, and responsible disclosure workflows.

This repository does **not** provide real-world exploit code, weaponized payloads, bypass techniques, persistence mechanisms, or instructions for unauthorized access. The project is designed to help defenders reason about unknown vulnerabilities through safe simulations, telemetry analysis, detection rules, and response playbooks.

## Why This Project Exists

Zero-day threats are difficult because defenders often have to act before a public CVE, vendor patch, or stable detection signature exists. ZeroDaySentinel explores how security teams can prepare for this uncertainty using:

- threat modeling,
- attack-surface analysis,
- synthetic log generation,
- defensive detection logic,
- Sigma/YARA-style rules,
- threat intelligence enrichment,
- incident response playbooks,
- responsible disclosure templates.

## Current Status

ZeroDaySentinel is currently in early active development.

The first milestone focuses on building a safe and reproducible defensive lab:

- repository foundation,
- ethical and legal boundaries,
- zero-day concept documentation,
- synthetic log generation,
- safe anomaly detection,
- initial Sigma/YARA-style examples,
- incident response documentation,
- responsible disclosure workflow.

## What This Project Is Not

This is **not** an exploit repository.

ZeroDaySentinel does not include:

- real zero-day exploit code,
- weaponized proof-of-concept payloads,
- unauthorized testing instructions,
- exploit chaining,
- stealth or persistence logic,
- detection evasion techniques,
- internet-wide scanning tools.

## Planned Modules

| Module | Purpose | Status |
|---|---|---|
| `docs/` | Zero-day concepts, threat modeling, ethical boundaries | Planned |
| `lab/` | Synthetic logs and safe detector experiments | Planned |
| `detection/` | Sigma/YARA-style defensive rules | Planned |
| `incident-response/` | Triage, containment, recovery playbooks | Planned |
| `disclosure/` | Responsible disclosure templates | Planned |
| `dashboard/` | Future visualization layer | Planned |
| `research/` | Notes, references, and methodology | Planned |

## Benchmarking Policy

Performance metrics will be published only after reproducible experiments are implemented.

Planned metrics include:

- precision,
- recall,
- F1-score,
- false positive rate,
- event processing latency,
- memory overhead,
- detection coverage.

No unverified benchmark claims are included in this repository.

## Ethical Notice

This project is intended only for defensive education, authorized research, and security awareness. All examples are synthetic, local, and intentionally non-weaponized.

## Roadmap

### v0.1 — Repository Foundation

- README
- SECURITY.md
- contributing guidelines
- ethical boundaries
- project structure
- initial CI workflow

### v0.2 — Synthetic Telemetry Lab

- synthetic normal logs
- synthetic suspicious logs
- safe log generator
- local detector prototype

### v0.3 — Detection Engineering

- Sigma-style rules
- YARA-style rules
- IOC examples
- MITRE ATT&CK mapping

### v0.4 — Response and Disclosure

- incident response playbooks
- responsible disclosure templates
- sample zero-day readiness report

### v0.5 — Dashboard Prototype

- local dashboard
- anomaly timeline
- rule hit visualization
- reproducible demo screenshots

## Quick Start

Run the first safe local demo:

```powershell
python lab/log-generator/generate_logs.py
python lab/detector/detector.py
```

Expected output:

```text
[ZeroDaySentinel] Generated synthetic events.
[ZeroDaySentinel] Detection completed.
[ZeroDaySentinel] Alerts generated.
```

Generated files:

- `lab/sample-logs/sample_events.jsonl`
- `reports/alerts.json`
- `reports/summary.json`

This demo uses only synthetic telemetry and non-weaponized defensive detection logic.

## Architecture Overview

ZeroDaySentinel is organized as a defensive detection lab. The current prototype follows a safe synthetic telemetry pipeline:

Synthetic Event Generator
→ sample_events.jsonl
→ Defensive Detector
→ Risk Scoring and Rule Matching
→ alerts.json and summary.json

The project intentionally avoids exploit development. It focuses on how defenders can reason about unknown or undisclosed threats using telemetry, detection logic, response playbooks, and responsible disclosure workflows.

See `docs/architecture.md` for more details.

## Demo Output

The current local demo analyzes synthetic events and produces defensive alerts.

Example result from the v0.2 prototype:

- Generated events: 120
- Events analyzed: 120
- Alerts generated: 25
- Output files: `reports/alerts.json` and `reports/summary.json`

See `docs/demo-output.md` for more details.

## Why Star This Project?

ZeroDaySentinel is designed as a clean, ethical, and reproducible defensive security project. It is useful for people interested in detection engineering, blue-team research, threat hunting, incident response, responsible disclosure, safe zero-day readiness modeling, and synthetic telemetry experiments.

The project does not rely on fake benchmark claims. Metrics and performance results will be added only when reproducible experiments are implemented.


## Command-Line Usage

ZeroDaySentinel can also be run through a small local CLI entry point:

```powershell
python sentinel.py --demo
```

To print the latest generated summary:

```powershell
python sentinel.py --summary
```

See `docs/cli.md` for more details.

## Project Tracking

- See `CHANGELOG.md` for version history.
- See `ROADMAP.md` for planned development.
