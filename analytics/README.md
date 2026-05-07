# Detection Analytics

This directory contains defensive analytics utilities for ZeroDaySentinel.

## Generate Triage Analytics

From the repository root:

```powershell
python sentinel.py --demo
python analytics/triage_analytics.py
```

The generated file is:

- `reports/triage_analytics.json`

## Analytics Output

The triage analytics summary includes:

- total synthetic events,
- total generated alerts,
- alert rate,
- alert priority distribution,
- top observed hosts,
- top observed users,
- event type counts,
- rule hit counts,
- recommended action counts,
- triage pressure score.

## Safety

The analytics workflow uses only synthetic local telemetry and defensive alert metadata. It does not include exploit code, payloads, bypass techniques, persistence logic, evasion logic, unauthorized testing instructions, or internet-wide scanning tools.
