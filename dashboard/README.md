# Dashboard Prototype

This directory contains the ZeroDaySentinel local dashboard prototype.

## Generate Dashboard

From the repository root:

```powershell
python sentinel.py --demo
python dashboard/generate_dashboard.py
```

The generated file is:

- `dashboard/index.html`

Open `dashboard/index.html` in a browser to view the local dashboard.

## Dashboard Contents

The dashboard summarizes:

- total synthetic events,
- total generated alerts,
- alert rate,
- alert priority distribution,
- event type distribution,
- defensive safety boundary.

## Safety

The dashboard is generated from synthetic telemetry only. It does not include exploit code, payloads, bypass techniques, persistence logic, evasion logic, unauthorized testing instructions, or internet-wide scanning tools.
